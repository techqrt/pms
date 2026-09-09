from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.lead.models.lead import Lead
from pms_apps.lead.serilizers.request.create import LeadCreateRequestSerilizer
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.marketing.models.marketing_employee import MarketingEmployee
from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager
from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee
from pms_apps.common.models.permissions import LeadPermission, PropertyPermission
from pms_apps.property.models.property import Property
from pms_apps.property.models.property_details import PropertyDetail
from pms_apps.property.models.property_assignment import PropertyAssignment


class LeadCountBreakdownTests(TestCase):
    """/lead/count/ must report a Tenant/Landlord breakdown and a conversion
    rate, where a lead counts as converted once it's actually linked to a
    property (Tenant via PropertyAssignment, Landlord via PropertyDetail)."""

    def setUp(self):
        self.caller = User.objects.create(name="Any User", phone_number="4000000000")
        creator = User.objects.create(name="Creator", phone_number="4000000001")

        def make_lead(phone, first_name, purpose):
            lead_user = User.objects.create(name=first_name, phone_number=phone, department=purpose)
            return Lead.objects.create(
                lead_id=lead_user, first_name=first_name, last_name="Test", purpose=purpose,
            )

        # Converted tenant: has a PropertyAssignment.
        self.converted_tenant = make_lead("4000000010", "ConvertedTenant", "Tenant")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)
        PropertyAssignment.objects.create(property=self.property, tenant=self.converted_tenant)

        # Unconverted tenant: no PropertyAssignment.
        self.unconverted_tenant = make_lead("4000000011", "UnconvertedTenant", "Tenant")

        # Converted landlord: owns a PropertyDetail.
        self.converted_landlord = make_lead("4000000012", "ConvertedLandlord", "Landlord")
        landlord_property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)
        PropertyDetail().create(
            property_id=landlord_property.property_id, building_name="Test Building",
            monthly_rent=0, security_deposit_amount=0, late_fee_type="Day wise", late_fee_value=0,
            current_status="Vacant", landlord_id=self.converted_landlord.lead_id_id, created_by_id=creator.user_id,
            address_line_1="", area_zone="", city="", state="", country="", pincode="",
        )

        # Unconverted landlord: no PropertyDetail.
        self.unconverted_landlord = make_lead("4000000013", "UnconvertedLandlord", "Landlord")

    def _client(self):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=self.caller)
        return client

    def test_count_returns_purpose_breakdown_and_conversion_rate(self):
        response = self._client().get("/lead/count/")
        self.assertEqual(response.status_code, 200, response.data)
        data = response.data["data"]
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["byPurpose"], {"Tenant": 2, "Landlord": 2})
        self.assertEqual(data["convertedCount"], 2)
        self.assertEqual(data["conversionRate"], 50.0)


class LeadCreateRequestSerilizerTests(TestCase):
    """Validation tests for Create Lead: only first_name, last_name,
    phone_number (contact number), purpose (lead type) and lead_category
    are mandatory; every other field must be optional."""

    def minimal_payload(self):
        return {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "purpose": "Tenant",
            "lead_category": "Bachelor",
        }

    def test_valid_minimal_lead(self):
        serializer = LeadCreateRequestSerilizer(data=self.minimal_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_optional_fields_omitted_succeeds(self):
        payload = self.minimal_payload()
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        for field in (
            "lead_origin", "nationality", "passport_or_id",
            "civil_id", "po_box", "feedback", "lead_assign_to",
            "address", "country", "city",
        ):
            self.assertNotIn(field, serializer.errors)

    def test_optional_fields_as_blank_strings_succeeds(self):
        payload = self.minimal_payload()
        payload.update({
            "passport_or_id": "",
            "civil_id": "",
            "po_box": "",
            "feedback": "",
            "lead_origin": "",
            "address": "",
        })
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_first_name_fails(self):
        payload = self.minimal_payload()
        del payload["first_name"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_missing_last_name_fails(self):
        payload = self.minimal_payload()
        del payload["last_name"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_missing_contact_number_fails(self):
        payload = self.minimal_payload()
        del payload["phone_number"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)

    def test_missing_lead_type_fails(self):
        payload = self.minimal_payload()
        del payload["purpose"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("purpose", serializer.errors)

    def test_missing_lead_category_fails(self):
        payload = self.minimal_payload()
        del payload["lead_category"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("lead_category", serializer.errors)

    def test_create_builds_request_with_none_for_omitted_optional_fields(self):
        serializer = LeadCreateRequestSerilizer(data=self.minimal_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)
        request = serializer.save()

        self.assertEqual(request.first_name, "John")
        self.assertEqual(request.last_name, "Doe")
        self.assertEqual(request.phone_number, "1234567890")
        self.assertEqual(request.purpose, "Tenant")
        self.assertEqual(request.lead_category, "Bachelor")
        self.assertIsNone(request.lead_origin)
        self.assertIsNone(request.nationality_id)
        self.assertIsNone(request.passport_or_id)
        self.assertIsNone(request.civil_id)
        self.assertIsNone(request.po_box)
        self.assertIsNone(request.feedback)
        self.assertIsNone(request.lead_assign_to)
        self.assertIsNone(request.address)
        self.assertIsNone(request.country_id)
        self.assertIsNone(request.city_id)


class LeadCreateEndpointTests(TestCase):
    """End-to-end smoke test hitting POST /lead/create/ through the real
    view/controller stack, not just the serializer in isolation."""

    def setUp(self):
        self.client = APIClient(HTTP_USER_AGENT="pytest")
        self.auth_user = User.objects.create(name="Auth User", phone_number="0000000000")
        self.client.force_authenticate(user=self.auth_user)

    def minimal_payload(self):
        return {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "purpose": "Tenant",
            "lead_category": "Bachelor",
        }

    def test_create_lead_with_only_mandatory_fields_returns_201(self):
        response = self.client.post("/lead/create/", data=self.minimal_payload(), format="json")
        self.assertEqual(response.status_code, 201, response.data)

        lead = Lead.objects.get(first_name="John", last_name="Doe")
        self.assertEqual(lead.purpose, "Tenant")
        self.assertEqual(lead.lead_category, "Bachelor")
        self.assertIsNone(lead.lead_origin)
        self.assertIsNone(lead.nationality_id)
        self.assertIsNone(lead.passport_or_id)
        self.assertIsNone(lead.civil_id)
        self.assertIsNone(lead.po_box)
        self.assertIsNone(lead.feedback)

    def test_create_lead_missing_mandatory_field_returns_400(self):
        payload = self.minimal_payload()
        del payload["first_name"]
        response = self.client.post("/lead/create/", data=payload, format="json")
        self.assertEqual(response.status_code, 400)


class LeadAssignmentAuthorizationTests(TestCase):
    """Assignment-based tenant/landlord visibility: a Marketing Employee may
    view/update only the leads (tenant or landlord) assigned to them via
    lead_assign_to; leads assigned to someone else must be fully denied,
    including by manipulating lead_id directly in the request."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Marketing Manager", phone_number="2000000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.manager_user.user_id, name="Marketing Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="Marketing Employee", phone_number="2000000002", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.employee_user.user_id, name="Marketing Employee", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_employee_user = User.objects.create(
            name="Other Marketing Employee", phone_number="2000000003", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Other Marketing Employee", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        def make_lead(phone, first_name, purpose, assign_to):
            lead_user = User.objects.create(name=first_name, phone_number=phone, department=purpose)
            return Lead.objects.create(
                lead_id=lead_user, first_name=first_name, last_name="Test", purpose=purpose,
                lead_assign_to=assign_to,
            )

        self.assigned_tenant = make_lead("2000000010", "AssignedTenant", "Tenant", self.employee_user)
        self.unassigned_tenant = make_lead("2000000011", "UnassignedTenant", "Tenant", self.other_employee_user)
        self.assigned_landlord = make_lead("2000000012", "AssignedLandlord", "Landlord", self.employee_user)
        self.unassigned_landlord = make_lead("2000000013", "UnassignedLandlord", "Landlord", self.other_employee_user)

        # A second, unrelated Manager/Employee pair - used to prove Manager
        # scoping stops at their own team and doesn't leak to other teams.
        self.unrelated_manager_user = User.objects.create(
            name="Unrelated Manager", phone_number="2000000020", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.unrelated_manager_user.user_id, name="Unrelated Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )
        self.unrelated_employee_user = User.objects.create(
            name="Unrelated Employee", phone_number="2000000021", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.unrelated_employee_user.user_id, name="Unrelated Employee", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.unrelated_manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )
        self.unrelated_tenant = make_lead("2000000022", "UnrelatedTenant", "Tenant", self.unrelated_employee_user)

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_employee_can_view_assigned_tenant(self):
        response = self._client_for(self.employee_user).get(
            f"/lead/get/?lead_id={self.assigned_tenant.lead_id_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_can_view_assigned_landlord(self):
        response = self._client_for(self.employee_user).get(
            f"/lead/get/?lead_id={self.assigned_landlord.lead_id_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_cannot_view_unassigned_tenant(self):
        response = self._client_for(self.employee_user).get(
            f"/lead/get/?lead_id={self.unassigned_tenant.lead_id_id}"
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_employee_cannot_view_unassigned_landlord(self):
        response = self._client_for(self.employee_user).get(
            f"/lead/get/?lead_id={self.unassigned_landlord.lead_id_id}"
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_employee_cannot_bypass_by_changing_lead_id(self):
        """Same request shape as the assigned-tenant call, only the ID differs -
        simulates an Employee editing the lead_id query param directly."""
        response = self._client_for(self.employee_user).get(
            f"/lead/get/?lead_id={self.unassigned_tenant.lead_id_id}"
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertNotIn("data", response.data or {})

    def test_employee_cannot_update_unassigned_tenant(self):
        response = self._client_for(self.employee_user).put(
            "/lead/update/",
            data={
                "lead_id": self.unassigned_tenant.lead_id_id, "first_name": "Hacked",
                "permissions": {"property": True},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.unassigned_tenant.refresh_from_db()
        self.assertEqual(self.unassigned_tenant.first_name, "UnassignedTenant")

    def test_employee_can_update_assigned_tenant(self):
        response = self._client_for(self.employee_user).put(
            "/lead/update/",
            data={
                "lead_id": self.assigned_tenant.lead_id_id, "first_name": "Updated",
                "permissions": {"property": True},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assigned_tenant.refresh_from_db()
        self.assertEqual(self.assigned_tenant.first_name, "Updated")

    def test_employee_get_all_only_returns_assigned_leads(self):
        response = self._client_for(self.employee_user).get("/lead/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [item["leadId"] for item in response.data["data"]["data"]]
        self.assertIn(self.assigned_tenant.lead_id_id, ids)
        self.assertIn(self.assigned_landlord.lead_id_id, ids)
        self.assertNotIn(self.unassigned_tenant.lead_id_id, ids)
        self.assertNotIn(self.unassigned_landlord.lead_id_id, ids)

    def test_manager_get_all_returns_leads_assigned_to_manager_or_their_employees(self):
        """A Manager must see leads assigned to any Employee reporting to them
        (not just leads assigned to the Manager themself), but never leads
        belonging to a different Manager's team."""
        response = self._client_for(self.manager_user).get("/lead/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [item["leadId"] for item in response.data["data"]["data"]]
        self.assertIn(self.assigned_tenant.lead_id_id, ids)
        self.assertIn(self.unassigned_tenant.lead_id_id, ids)
        self.assertNotIn(self.unrelated_tenant.lead_id_id, ids)


class ManagerAssignmentVisibilityTests(TestCase):
    """Phase 5: a lead a Manager creates and assigns to a specific Employee
    must become visible to that Employee, and to no other Employee, end to
    end through the real POST /lead/create/ -> GET /lead/get/ flow."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Marketing Manager", phone_number="3000000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.manager_user.user_id, name="Marketing Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.assignee_employee = User.objects.create(
            name="Assignee Employee", phone_number="3000000002", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.assignee_employee.user_id, name="Assignee Employee", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_employee = User.objects.create(
            name="Other Employee", phone_number="3000000003", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.other_employee.user_id, name="Other Employee", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_assigned_lead_visible_to_assignee_and_not_others(self):
        create_response = self._client_for(self.manager_user).post(
            "/lead/create/",
            data={
                "first_name": "Manager", "last_name": "Assigned", "phone_number": "3000000010",
                "purpose": "Tenant", "lead_category": "Bachelor",
                "lead_assign_to": {"user_id": self.assignee_employee.user_id},
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201, create_response.data)
        lead_id = create_response.data["data"]["lead_id"]

        assignee_view = self._client_for(self.assignee_employee).get(f"/lead/get/?lead_id={lead_id}")
        self.assertEqual(assignee_view.status_code, 200, assignee_view.data)

        other_view = self._client_for(self.other_employee).get(f"/lead/get/?lead_id={lead_id}")
        self.assertEqual(other_view.status_code, 400, other_view.data)

        assignee_list = self._client_for(self.assignee_employee).get("/lead/get_all/")
        assignee_ids = [item["leadId"] for item in assignee_list.data["data"]["data"]]
        self.assertIn(lead_id, assignee_ids)

        other_list = self._client_for(self.other_employee).get("/lead/get_all/")
        other_ids = [item["leadId"] for item in other_list.data["data"]["data"]]
        self.assertNotIn(lead_id, other_ids)

    def test_employee_created_lead_visible_to_their_manager(self):
        """Issue 2: a lead an Employee creates and assigns to themself must
        be visible to their Lead Manager, via both get_all and count."""
        create_response = self._client_for(self.assignee_employee).post(
            "/lead/create/",
            data={
                "first_name": "Employee", "last_name": "Created", "phone_number": "3000000011",
                "purpose": "Tenant", "lead_category": "Bachelor",
                "lead_assign_to": {"user_id": self.assignee_employee.user_id},
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201, create_response.data)
        lead_id = create_response.data["data"]["lead_id"]

        manager_list = self._client_for(self.manager_user).get("/lead/get_all/")
        self.assertEqual(manager_list.status_code, 200, manager_list.data)
        manager_ids = [item["leadId"] for item in manager_list.data["data"]["data"]]
        self.assertIn(lead_id, manager_ids)

        manager_count = self._client_for(self.manager_user).get("/lead/count/")
        self.assertEqual(manager_count.status_code, 200, manager_count.data)
        self.assertGreaterEqual(manager_count.data["data"]["count"], 1)


class LeadSecurityRegressionTests(TestCase):
    """Phase 8: direct-API-bypass checks for the tenant/landlord (Lead)
    authorization changes - no valid JWT means no access."""

    def setUp(self):
        lead_user = User.objects.create(name="SomeLead", phone_number="5000000001", department="Tenant")
        self.lead = Lead.objects.create(lead_id=lead_user, first_name="Some", last_name="Lead", purpose="Tenant")
        self.client = APIClient(HTTP_USER_AGENT="pytest")  # deliberately not authenticated

    def test_unauthenticated_get_rejected(self):
        response = self.client.get(f"/lead/get/?lead_id={self.lead.lead_id_id}")
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_get_all_rejected(self):
        response = self.client.get("/lead/get_all/")
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_update_rejected(self):
        response = self.client.put(
            "/lead/update/",
            data={"lead_id": self.lead.lead_id_id, "first_name": "Should Not Apply"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.lead.refresh_from_db()
        self.assertNotEqual(self.lead.first_name, "Should Not Apply")


class CheckInCheckOutLeadAuthorizationTests(TestCase):
    """GAP-013 (lead side): the same assignment-based tenant/landlord
    visibility rule that already applies to Marketing must also apply to
    Check-In Check-Out staff, since their team now gets assigned tenants too."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.cico_manager = User.objects.create(
            name="CICO Manager", phone_number="9600000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.cico_manager.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.cico_employee = User.objects.create(
            name="CICO Employee", phone_number="9600000002", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.cico_employee.user_id, name="CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.cico_manager.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_cico_employee = User.objects.create(
            name="Other CICO Employee", phone_number="9600000003", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.other_cico_employee.user_id, name="Other CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.cico_manager.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        tenant_user = User.objects.create(name="CICO Tenant", phone_number="9600000004", department="Tenant")
        self.tenant = Lead.objects.create(
            lead_id=tenant_user, first_name="CICO", last_name="Tenant", purpose="Tenant",
            lead_assign_to=self.cico_employee,
        )

        # A second, unrelated CICO Manager/Employee pair to prove scoping
        # stops at the Manager's own team.
        self.unrelated_cico_manager = User.objects.create(
            name="Unrelated CICO Manager", phone_number="9600000010", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.unrelated_cico_manager.user_id, name="Unrelated CICO Manager", dob=None,
            department="Check-In Check-Out", team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )
        self.unrelated_cico_employee = User.objects.create(
            name="Unrelated CICO Employee", phone_number="9600000011", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.unrelated_cico_employee.user_id, name="Unrelated CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.unrelated_cico_manager.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )
        unrelated_tenant_user = User.objects.create(
            name="Unrelated CICO Tenant", phone_number="9600000012", department="Tenant"
        )
        self.unrelated_tenant = Lead.objects.create(
            lead_id=unrelated_tenant_user, first_name="Unrelated", last_name="Tenant", purpose="Tenant",
            lead_assign_to=self.unrelated_cico_employee,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_assigned_cico_employee_can_view_tenant(self):
        response = self._client_for(self.cico_employee).get(
            f"/lead/get/?lead_id={self.tenant.lead_id_id}&values=firstName,lastName"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_unassigned_cico_employee_cannot_view_tenant(self):
        response = self._client_for(self.other_cico_employee).get(
            f"/lead/get/?lead_id={self.tenant.lead_id_id}&values=firstName,lastName"
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_cico_employee_get_all_only_returns_assigned_leads(self):
        response = self._client_for(self.cico_employee).get("/lead/get_all/?values=leadId")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [item["leadId"] for item in response.data["data"]["data"]]
        self.assertEqual(ids, [self.tenant.lead_id_id])

    def test_cico_manager_get_all_scoped_to_managers_own_assignments(self):
        """A CICO Manager sees leads assigned to their own team (including
        employees), but never a different Manager's team."""
        response = self._client_for(self.cico_manager).get("/lead/get_all/?values=leadId")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [item["leadId"] for item in response.data["data"]["data"]]
        self.assertIn(self.tenant.lead_id_id, ids)
        self.assertNotIn(self.unrelated_tenant.lead_id_id, ids)


class LeadGetAllPaginationTests(TestCase):
    """The shared GetAllSerializer/GetAll pagination fix (page_num/limit
    validation + limit clamp) must apply here too, since /lead/get_all/
    reuses that same shared infrastructure."""

    def setUp(self):
        self.user = User.objects.create(name="Any User", phone_number="9999900002")

    def _client(self):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=self.user)
        return client

    def test_page_num_zero_returns_field_validation_error(self):
        response = self._client().get("/lead/get_all/?page_num=0")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("page_num", response.data["error"][0])

    def test_limit_zero_returns_field_validation_error(self):
        response = self._client().get("/lead/get_all/?limit=0")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("limit", response.data["error"][0])

    def test_excessive_limit_does_not_error(self):
        response = self._client().get("/lead/get_all/?limit=999999999")
        self.assertEqual(response.status_code, 200, response.data)
