from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.property.models.property import Property
from pms_apps.property.models.property_details import PropertyDetail
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.marketing.models.marketing_employee import MarketingEmployee
from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager
from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee
from pms_apps.common.models.permissions import LeadPermission, PropertyPermission
from pms_apps.lead.models.lead import Lead


class PropertyMarketingAuthorizationTests(TestCase):
    """Marketing Employees can view every property but cannot edit any of them;
    Marketing Managers can view and edit every property. Non-Marketing users'
    existing behaviour is unaffected by this change."""

    def setUp(self):
        # A property this test's users neither created, are assigned to, nor own as landlord.
        other_owner = User.objects.create(name="Other Owner", phone_number="9990001111")
        self.property = Property.objects.create(
            rental_type="Flat", rental_for="Family", created_by=other_owner,
        )

        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Marketing Manager", phone_number="1000000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.manager_user.user_id, name="Marketing Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="Marketing Employee", phone_number="1000000002", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.employee_user.user_id, name="Marketing Employee", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        # A non-Marketing user with no relation to the property, to confirm the
        # existing (unrestricted-update / scoped-view) behaviour is unchanged.
        self.other_dept_user = User.objects.create(
            name="Other Dept User", phone_number="1000000003", department="IT", role="Employee"
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_marketing_employee_can_view_unassigned_property(self):
        response = self._client_for(self.employee_user).get(
            f"/property/get/?property_id={self.property.property_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_marketing_employee_sees_unassigned_property_in_list(self):
        response = self._client_for(self.employee_user).get("/property/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [p["propertyId"] for p in response.data["data"]["data"]]
        self.assertIn(self.property.property_id, ids)

    def test_marketing_manager_can_view_unassigned_property(self):
        response = self._client_for(self.manager_user).get(
            f"/property/get/?property_id={self.property.property_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_marketing_employee_cannot_edit_property(self):
        response = self._client_for(self.employee_user).put(
            "/property/update/",
            data={"property_id": self.property.property_id, "block": "Blocked Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.property.refresh_from_db()
        self.assertNotEqual(self.property.block, "Blocked Edit")

    def test_marketing_manager_can_edit_property(self):
        response = self._client_for(self.manager_user).put(
            "/property/update/",
            data={"property_id": self.property.property_id, "block": "Manager Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.property.refresh_from_db()
        self.assertEqual(self.property.block, "Manager Edit")

    def test_non_marketing_user_update_behaviour_unchanged(self):
        """No authorization existed for non-Marketing users before this change;
        this documents that update still succeeds for them (out of scope here)."""
        response = self._client_for(self.other_dept_user).put(
            "/property/update/",
            data={"property_id": self.property.property_id, "block": "Other Dept Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_non_marketing_user_view_still_scoped(self):
        """A non-Marketing user with no created_by/assigned_to/landlord relation
        to the property is still blocked from viewing it (unchanged behaviour)."""
        response = self._client_for(self.other_dept_user).get(
            f"/property/get/?property_id={self.property.property_id}"
        )
        self.assertEqual(response.status_code, 400, response.data)


class PropertySecurityRegressionTests(TestCase):
    """Phase 8: direct-API-bypass checks. Authorization must be enforced
    server-side regardless of how the request is made - no valid JWT means
    no access, full stop, for every endpoint these authorization changes
    touch."""

    def setUp(self):
        creator = User.objects.create(name="Creator", phone_number="5000000000")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)
        self.client = APIClient(HTTP_USER_AGENT="pytest")  # deliberately not authenticated

    def test_unauthenticated_get_rejected(self):
        response = self.client.get(f"/property/get/?property_id={self.property.property_id}")
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_get_all_rejected(self):
        response = self.client.get("/property/get_all/")
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_update_rejected(self):
        response = self.client.put(
            "/property/update/",
            data={"property_id": self.property.property_id, "block": "Should Not Apply"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.property.refresh_from_db()
        self.assertNotEqual(self.property.block, "Should Not Apply")


class PropertyLandlordRedactionTests(TestCase):
    """A Marketing Employee viewing a property must see the landlord's name
    only unless that landlord is assigned to them (lead_assign_to == the
    employee), in which case they get full contact details - same as
    Managers, who always see full details."""

    def setUp(self):
        creator = User.objects.create(name="Creator", phone_number="7000000000")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)

        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Marketing Manager", phone_number="7000000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.manager_user.user_id, name="Marketing Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="Marketing Employee", phone_number="7000000002", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.employee_user.user_id, name="Marketing Employee", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        landlord_user = User.objects.create(
            name="Landlord Person", phone_number="7000000003", email="landlord@example.com", department="Landlord"
        )
        self.landlord = Lead.objects.create(
            lead_id=landlord_user, first_name="Landlord", last_name="Person", purpose="Landlord",
        )
        PropertyDetail().create(
            property_id=self.property.property_id, building_name="Test Building",
            monthly_rent=0, security_deposit_amount=0, late_fee_type="Day wise", late_fee_value=0,
            current_status="Vacant", landlord_id=self.landlord.lead_id_id, created_by_id=creator.user_id,
            address_line_1="", area_zone="", city="", state="", country="", pincode="",
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_unassigned_employee_sees_landlord_name_only(self):
        response = self._client_for(self.employee_user).get(f"/property/get/?property_id={self.property.property_id}")
        self.assertEqual(response.status_code, 200, response.data)
        landlord = response.data["data"]["landlord"]
        self.assertEqual(landlord["name"], "Landlord Person")
        self.assertIsNone(landlord["phoneNumber"])
        self.assertIsNone(landlord["email"])

    def test_assigned_employee_sees_full_landlord_details(self):
        self.landlord.lead_assign_to = self.employee_user
        self.landlord.save(update_fields=["lead_assign_to"])

        response = self._client_for(self.employee_user).get(f"/property/get/?property_id={self.property.property_id}")
        self.assertEqual(response.status_code, 200, response.data)
        landlord = response.data["data"]["landlord"]
        self.assertEqual(landlord["name"], "Landlord Person")
        self.assertEqual(landlord["phoneNumber"], "7000000003")
        self.assertEqual(landlord["email"], "landlord@example.com")

    def test_manager_always_sees_full_landlord_details(self):
        response = self._client_for(self.manager_user).get(f"/property/get/?property_id={self.property.property_id}")
        self.assertEqual(response.status_code, 200, response.data)
        landlord = response.data["data"]["landlord"]
        self.assertEqual(landlord["phoneNumber"], "7000000003")
        self.assertEqual(landlord["email"], "landlord@example.com")

    def test_unassigned_employee_sees_landlord_name_only_in_list(self):
        response = self._client_for(self.employee_user).get("/property/get_all/?limit=2000")
        self.assertEqual(response.status_code, 200, response.data)
        row = next(p for p in response.data["data"]["data"] if p["propertyId"] == self.property.property_id)
        self.assertEqual(row["landlord"]["name"], "Landlord Person")
        self.assertIsNone(row["landlord"]["phoneNumber"])
        self.assertIsNone(row["landlord"]["email"])


class PropertyAssignmentAuthorizationTests(TestCase):
    """A Marketing Employee may only link a property to a tenant (create or
    update a PropertyAssignment) when they are the assigned handler for BOTH
    that property and that tenant. Managers are unrestricted."""

    def setUp(self):
        creator = User.objects.create(name="Creator", phone_number="8000000000")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)

        landlord_user = User.objects.create(name="Test Landlord", phone_number="8000000008", department="Landlord")
        landlord = Lead.objects.create(
            lead_id=landlord_user, first_name="Test", last_name="Landlord", purpose="Landlord",
        )
        PropertyDetail().create(
            property_id=self.property.property_id, building_name="Test Building",
            monthly_rent=0, security_deposit_amount=0, late_fee_type="Day wise", late_fee_value=0,
            current_status="Vacant", landlord_id=landlord.lead_id_id, created_by_id=creator.user_id,
            address_line_1="", area_zone="", city="", state="", country="", pincode="",
        )

        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Marketing Manager", phone_number="8000000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.manager_user.user_id, name="Marketing Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        def make_employee(phone):
            u = User.objects.create(name=f"Employee {phone}", phone_number=phone, department="Marketing", role="Employee")
            MarketingEmployee().create(
                employee_id=u.user_id, name=f"Employee {phone}", dob=None, designation="",
                department="Marketing", campaigns_assigned=0, leads_generated=0,
                manager_ref=self.manager_user.user_id,
                lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
            )
            return u

        self.both_assigned_employee = make_employee("8000000002")
        self.property_only_employee = make_employee("8000000003")
        self.tenant_only_employee = make_employee("8000000004")
        self.neither_assigned_employee = make_employee("8000000005")

        self.property.assigned_to.add(self.both_assigned_employee, self.property_only_employee)

        tenant_user = User.objects.create(name="Test Tenant", phone_number="8000000006", department="Tenant")
        self.tenant = Lead.objects.create(
            lead_id=tenant_user, first_name="Test", last_name="Tenant", purpose="Tenant",
            lead_assign_to=self.both_assigned_employee,
        )

        tenant2_user = User.objects.create(name="Test Tenant 2", phone_number="8000000007", department="Tenant")
        self.tenant_assigned_to_tenant_only_employee = Lead.objects.create(
            lead_id=tenant2_user, first_name="Test2", last_name="Tenant", purpose="Tenant",
            lead_assign_to=self.tenant_only_employee,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def _assign_payload(self, tenant):
        return {
            "property_id": self.property.property_id, "tenant_id": tenant.lead_id_id,
            "assigned_by_id": self.manager_user.user_id,
        }

    def test_employee_assigned_to_both_can_assign_property_to_tenant(self):
        response = self._client_for(self.both_assigned_employee).post(
            "/property/assign/", data=self._assign_payload(self.tenant), format="json"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_assigned_to_property_only_cannot_assign(self):
        response = self._client_for(self.property_only_employee).post(
            "/property/assign/", data=self._assign_payload(self.tenant), format="json"
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_employee_assigned_to_tenant_only_cannot_assign(self):
        response = self._client_for(self.tenant_only_employee).post(
            "/property/assign/", data=self._assign_payload(self.tenant_assigned_to_tenant_only_employee), format="json"
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_employee_assigned_to_neither_cannot_assign(self):
        response = self._client_for(self.neither_assigned_employee).post(
            "/property/assign/", data=self._assign_payload(self.tenant), format="json"
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_manager_can_assign_regardless_of_assignment(self):
        response = self._client_for(self.manager_user).post(
            "/property/assign/", data=self._assign_payload(self.tenant), format="json"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_assigned_to_both_can_update_assignment(self):
        create_response = self._client_for(self.both_assigned_employee).post(
            "/property/assign/", data=self._assign_payload(self.tenant), format="json"
        )
        assignment_id = create_response.data["data"]["property_assignment_id"]

        update_response = self._client_for(self.both_assigned_employee).patch(
            "/property/assignment/update/",
            data={"property_assignment_id": assignment_id, "internal_notes": "Updated by owner"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200, update_response.data)

    def test_employee_assigned_to_neither_cannot_update_assignment(self):
        create_response = self._client_for(self.manager_user).post(
            "/property/assign/", data=self._assign_payload(self.tenant), format="json"
        )
        assignment_id = create_response.data["data"]["property_assignment_id"]

        update_response = self._client_for(self.neither_assigned_employee).patch(
            "/property/assignment/update/",
            data={"property_assignment_id": assignment_id, "internal_notes": "Should Not Apply"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 400, update_response.data)


class PropertyCreatorEditDeleteTests(TestCase):
    """GAP-008/GAP-009/GAP-011: a Marketing Employee may create properties
    (creation itself was never restricted, and stays that way) and keeps
    edit AND delete rights on a property they created or are an assigned
    handler of (Property.assigned_to) - the same ownership rule applies to
    both actions, symmetrically. Any other property remains Manager-only for
    both edit and delete."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Marketing Manager", phone_number="9000000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.manager_user.user_id, name="Marketing Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        def make_employee(phone):
            u = User.objects.create(name=f"Employee {phone}", phone_number=phone, department="Marketing", role="Employee")
            MarketingEmployee().create(
                employee_id=u.user_id, name=f"Employee {phone}", dob=None, designation="",
                department="Marketing", campaigns_assigned=0, leads_generated=0,
                manager_ref=self.manager_user.user_id,
                lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
            )
            return u

        self.creator_employee = make_employee("9000000002")
        self.other_employee = make_employee("9000000003")
        self.assigned_only_employee = make_employee("9000000004")

        # Simulates a property the Employee created via POST /property/create/
        # (created_by=creator_employee, as the endpoint already sets it to the
        # requester automatically).
        self.own_property = Property.objects.create(
            rental_type="Flat", rental_for="Family", created_by=self.creator_employee,
        )

        # A separate property the creator has no relation to, but that a
        # different employee is only assigned to (not the creator) - proves
        # the assigned_to branch of the ownership rule independently.
        other_creator = User.objects.create(name="Other Creator", phone_number="9000000005")
        self.assigned_property = Property.objects.create(
            rental_type="Flat", rental_for="Family", created_by=other_creator,
        )
        self.assigned_property.assigned_to.add(self.assigned_only_employee)

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_creator_employee_can_edit_own_property(self):
        response = self._client_for(self.creator_employee).put(
            "/property/update/",
            data={"property_id": self.own_property.property_id, "block": "Creator Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.own_property.refresh_from_db()
        self.assertEqual(self.own_property.block, "Creator Edit")

    def test_assigned_only_employee_can_edit_property(self):
        response = self._client_for(self.assigned_only_employee).put(
            "/property/update/",
            data={"property_id": self.assigned_property.property_id, "block": "Assignee Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_other_employee_cannot_edit_creators_property(self):
        response = self._client_for(self.other_employee).put(
            "/property/update/",
            data={"property_id": self.own_property.property_id, "block": "Should Not Apply"},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.own_property.refresh_from_db()
        self.assertNotEqual(self.own_property.block, "Should Not Apply")

    def test_manager_can_still_edit_employees_property(self):
        response = self._client_for(self.manager_user).put(
            "/property/update/",
            data={"property_id": self.own_property.property_id, "block": "Manager Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_creator_employee_can_delete_own_property(self):
        """GAP-011: delete must honor the same creator/assignee exception as edit."""
        response = self._client_for(self.creator_employee).delete(
            f"/property/delete/?property_id={self.own_property.property_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.own_property.refresh_from_db()
        self.assertFalse(self.own_property.is_active)

    def test_assigned_only_employee_can_delete_property(self):
        response = self._client_for(self.assigned_only_employee).delete(
            f"/property/delete/?property_id={self.assigned_property.property_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_other_employee_cannot_delete_creators_property(self):
        response = self._client_for(self.other_employee).delete(
            f"/property/delete/?property_id={self.own_property.property_id}"
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue(Property.objects.filter(property_id=self.own_property.property_id, is_active=True).exists())

    def test_employee_can_delete_many_of_their_own(self):
        response = self._client_for(self.creator_employee).patch(
            "/property/delete_many/",
            data={"property_ids": [self.own_property.property_id]},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_cannot_delete_many_including_unowned_property(self):
        """All-or-nothing: if even one property in the batch isn't theirs, the whole request is blocked."""
        response = self._client_for(self.creator_employee).patch(
            "/property/delete_many/",
            data={"property_ids": [self.own_property.property_id, self.assigned_property.property_id]},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue(Property.objects.filter(property_id=self.own_property.property_id, is_active=True).exists())

    def test_manager_can_delete_property(self):
        response = self._client_for(self.manager_user).delete(
            f"/property/delete/?property_id={self.own_property.property_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.own_property.refresh_from_db()
        self.assertFalse(self.own_property.is_active)


class PropertyCrossDepartmentAuthorizationTests(TestCase):
    """GAP-013: the same created_by/assigned_to ownership rule that governs
    Marketing Employee property edit/delete access must also apply to
    Check-In Check-Out Employees - it must NOT be possible for an unrelated
    Employee from either department to edit/delete a property just because
    the previous fix only checked Marketing."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        creator = User.objects.create(name="Creator", phone_number="9500000000")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)

        self.cico_manager = User.objects.create(
            name="CICO Manager", phone_number="9500000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.cico_manager.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.cico_employee_unassigned = User.objects.create(
            name="CICO Employee Unassigned", phone_number="9500000002", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.cico_employee_unassigned.user_id, name="CICO Employee Unassigned", dob=None,
            designation="", department="Check-In Check-Out", manager_ref=self.cico_manager.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.cico_employee_assigned = User.objects.create(
            name="CICO Employee Assigned", phone_number="9500000003", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.cico_employee_assigned.user_id, name="CICO Employee Assigned", dob=None,
            designation="", department="Check-In Check-Out", manager_ref=self.cico_manager.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )
        self.property.assigned_to.add(self.cico_employee_assigned)

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_unassigned_cico_employee_cannot_edit_property(self):
        """This is the exact GAP-013 reproduction: an unrelated Check-In
        Check-Out Employee must be blocked, same as an unrelated Marketing
        Employee already was."""
        response = self._client_for(self.cico_employee_unassigned).put(
            "/property/update/",
            data={"property_id": self.property.property_id, "monthly_rent": "8888"},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_unassigned_cico_employee_cannot_delete_property(self):
        response = self._client_for(self.cico_employee_unassigned).delete(
            f"/property/delete/?property_id={self.property.property_id}"
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue(Property.objects.filter(property_id=self.property.property_id, is_active=True).exists())

    def test_assigned_cico_employee_can_edit_property(self):
        """Confirms the fix is a real ownership check, not a blanket block -
        a CICO Employee assigned to this property (for their check-in work)
        keeps edit access, mirroring the Marketing Employee rule exactly."""
        response = self._client_for(self.cico_employee_assigned).put(
            "/property/update/",
            data={"property_id": self.property.property_id, "block": "CICO Assignee Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_cico_manager_can_edit_any_property(self):
        response = self._client_for(self.cico_manager).put(
            "/property/update/",
            data={"property_id": self.property.property_id, "block": "CICO Manager Edit"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)


class PropertyGetAllPaginationTests(TestCase):
    """GAP-005/GAP-006: invalid page_num/limit must return a normal
    field-validation error (not a raw exception like 'division by zero'),
    and an excessive limit must be silently capped server-side rather than
    returning the entire table in one response."""

    def setUp(self):
        self.user = User.objects.create(name="Any User", phone_number="9999900001")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=self.user)

    def _client(self):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=self.user)
        return client

    def test_page_num_zero_returns_field_validation_error(self):
        response = self._client().get("/property/get_all/?page_num=0&limit=2")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("page_num", response.data["error"][0])

    def test_page_num_negative_returns_field_validation_error(self):
        response = self._client().get("/property/get_all/?page_num=-1&limit=2")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("page_num", response.data["error"][0])

    def test_limit_zero_returns_field_validation_error_not_division_by_zero(self):
        response = self._client().get("/property/get_all/?page_num=1&limit=0")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("limit", response.data["error"][0])

    def test_excessive_limit_is_silently_capped(self):
        """Requesting far more than the server cap must not error - it should
        just come back capped, same as any other successful list call."""
        with patch("pms_apps.property.dataclasses.requests.get_all_property.Configurations.max_pagination_limit", 2):
            for i in range(3):
                Property.objects.create(rental_type="Flat", rental_for="Family", created_by=self.user)
            response = self._client().get("/property/get_all/?page_num=1&limit=999999999")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data["data"]["data"]), 2)


class PropertyGetTenantFieldTests(TestCase):
    """property/get/ must include the currently assigned tenant's basic
    details (via PropertyAssignment), or a blank object if no tenant is
    currently assigned."""

    def setUp(self):
        self.creator = User.objects.create(name="Creator", phone_number="7100000000")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=self.creator)
        self.client_ = APIClient(HTTP_USER_AGENT="pytest")
        self.client_.force_authenticate(user=self.creator)

    def test_no_assignment_returns_blank_tenant(self):
        response = self.client_.get(f"/property/get/?property_id={self.property.property_id}")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["data"]["tenant"], {})

    def test_active_assignment_returns_tenant_details(self):
        from pms_apps.property.models.property_assignment import PropertyAssignment

        tenant_user = User.objects.create(name="Tenant Person", phone_number="7100000001", department="Tenant")
        tenant_lead = Lead.objects.create(
            lead_id=tenant_user, first_name="Tenant", last_name="Person", purpose="Tenant",
        )
        PropertyAssignment.objects.create(property=self.property, tenant=tenant_lead)

        response = self.client_.get(f"/property/get/?property_id={self.property.property_id}")
        self.assertEqual(response.status_code, 200, response.data)
        tenant = response.data["data"]["tenant"]
        self.assertEqual(tenant["tenantId"], tenant_lead.lead_id_id)
        self.assertEqual(tenant["firstName"], "Tenant")
        self.assertEqual(tenant["phoneNumber"], "7100000001")

    def test_completed_assignment_does_not_count_as_current_tenant(self):
        from pms_apps.property.models.property_assignment import PropertyAssignment

        tenant_user = User.objects.create(name="Past Tenant", phone_number="7100000002", department="Tenant")
        tenant_lead = Lead.objects.create(
            lead_id=tenant_user, first_name="Past", last_name="Tenant", purpose="Tenant",
        )
        PropertyAssignment.objects.create(property=self.property, tenant=tenant_lead, assignment_status="Completed")

        response = self.client_.get(f"/property/get/?property_id={self.property.property_id}")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["data"]["tenant"], {})
