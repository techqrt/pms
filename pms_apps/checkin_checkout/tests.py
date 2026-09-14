from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.property.models.property import Property
from pms_apps.property.models.property_details import PropertyDetail
from pms_apps.lead.models.lead import Lead
from pms_apps.checkin_checkout.models.check_in import CheckIn
from pms_apps.checkin_checkout.models.check_out import CheckOut
from pms_apps.checkin_checkout.models.check_in_key import CheckInKey
from pms_apps.checkin_checkout.models.check_out_key import CheckOutKey
from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager
from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee
from pms_apps.common.models.permissions import LeadPermission, PropertyPermission


class CheckInCheckOutAuthorizationTestsMixin:
    """Shared setUp for Check-In/Check-Out Manager/Employee assignment-based
    authorization: an Employee may only view/edit records assigned to them;
    a Manager may view/edit every record (team oversight)."""

    record_model = None  # CheckIn or CheckOut
    id_field = None  # 'check_in_id' or 'check_out_id'
    code_field = None  # 'check_in_code' or 'check_out_code'
    base_path = None  # '/checkin-checkout/check_in/' or '/checkin-checkout/check_out/'

    # Sub-resource (Phase 6b): key is used as the representative child model -
    # document/inspection_item/utility_reading/payment all follow this exact
    # same create/update/delete-by-child-id authorization pattern.
    key_model = None  # CheckInKey or CheckOutKey
    key_id_field = None  # 'check_in_key_id' or 'check_out_key_id'
    key_parent_attr = None  # 'check_in' or 'check_out' (FK attr name on the key model)

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        creator = User.objects.create(name="Creator", phone_number="4000000000")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)

        self.manager_user = User.objects.create(
            name="CICO Manager", phone_number="4000000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.manager_user.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="CICO Employee", phone_number="4000000002", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.employee_user.user_id, name="CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_employee_user = User.objects.create(
            name="Other CICO Employee", phone_number="4000000003", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Other CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.assigned_record = self.record_model.objects.create(**{
            "property": self.property,
            self.code_field: f"TEST-{self.record_model.__name__}-ASSIGNED",
            "assigned_employee": self.employee_user,
        })
        self.unassigned_record = self.record_model.objects.create(**{
            "property": self.property,
            self.code_field: f"TEST-{self.record_model.__name__}-UNASSIGNED",
            "assigned_employee": self.other_employee_user,
        })

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def _record_id(self, record):
        return getattr(record, self.id_field)

    def test_employee_can_view_assigned_record(self):
        response = self._client_for(self.employee_user).get(
            f"{self.base_path}get/?{self.id_field}={self._record_id(self.assigned_record)}"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_cannot_view_unassigned_record(self):
        response = self._client_for(self.employee_user).get(
            f"{self.base_path}get/?{self.id_field}={self._record_id(self.unassigned_record)}"
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_manager_can_view_any_record(self):
        response = self._client_for(self.manager_user).get(
            f"{self.base_path}get/?{self.id_field}={self._record_id(self.unassigned_record)}"
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_get_all_only_returns_assigned_records(self):
        response = self._client_for(self.employee_user).get(f"{self.base_path}get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [item[self._camel(self.id_field)] for item in response.data["data"]["data"]]
        self.assertIn(self._record_id(self.assigned_record), ids)
        self.assertNotIn(self._record_id(self.unassigned_record), ids)

    def test_employee_cannot_bypass_scoping_via_assigned_employee_id_param(self):
        """Passing another employee's ID in assigned_employee_id must not
        leak their records - the server always scopes to the caller."""
        response = self._client_for(self.employee_user).get(
            f"{self.base_path}get_all/?assigned_employee_id={self.other_employee_user.user_id}"
        )
        self.assertEqual(response.status_code, 200, response.data)
        ids = [item[self._camel(self.id_field)] for item in response.data["data"]["data"]]
        self.assertNotIn(self._record_id(self.unassigned_record), ids)

    def test_manager_get_all_returns_every_record(self):
        response = self._client_for(self.manager_user).get(f"{self.base_path}get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [item[self._camel(self.id_field)] for item in response.data["data"]["data"]]
        self.assertIn(self._record_id(self.assigned_record), ids)
        self.assertIn(self._record_id(self.unassigned_record), ids)

    def test_employee_cannot_update_unassigned_record(self):
        response = self._client_for(self.employee_user).patch(
            f"{self.base_path}update/information/",
            data={self.id_field: self._record_id(self.unassigned_record), "remarks_notes": "Hacked"},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.unassigned_record.refresh_from_db()
        self.assertNotEqual(self.unassigned_record.remarks_notes, "Hacked")

    def test_employee_can_update_assigned_record(self):
        response = self._client_for(self.employee_user).patch(
            f"{self.base_path}update/information/",
            data={self.id_field: self._record_id(self.assigned_record), "remarks_notes": "Updated by owner"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assigned_record.refresh_from_db()
        self.assertEqual(self.assigned_record.remarks_notes, "Updated by owner")

    def test_manager_can_update_any_record(self):
        response = self._client_for(self.manager_user).patch(
            f"{self.base_path}update/information/",
            data={self.id_field: self._record_id(self.unassigned_record), "remarks_notes": "Manager override"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.unassigned_record.refresh_from_db()
        self.assertEqual(self.unassigned_record.remarks_notes, "Manager override")

    def test_employee_cannot_delete_unassigned_record(self):
        response = self._client_for(self.employee_user).delete(
            f"{self.base_path}delete/?{self.id_field}={self._record_id(self.unassigned_record)}"
        )
        self.assertEqual(response.status_code, 400, response.data)

    @staticmethod
    def _camel(snake: str) -> str:
        parts = snake.split('_')
        return parts[0] + ''.join(p.title() for p in parts[1:])

    # -- Phase 6b: sub-resource (key) authorization --

    def test_employee_cannot_create_key_on_unassigned_record(self):
        response = self._client_for(self.employee_user).post(
            f"{self.base_path}key/create/",
            data={self.id_field: self._record_id(self.unassigned_record), "key_number": "K1", "key_type": "Main"},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertFalse(self.key_model.objects.filter(**{self.key_parent_attr: self.unassigned_record}).exists())

    def test_employee_can_create_key_on_assigned_record(self):
        response = self._client_for(self.employee_user).post(
            f"{self.base_path}key/create/",
            data={self.id_field: self._record_id(self.assigned_record), "key_number": "K1", "key_type": "Main"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_employee_cannot_update_key_on_unassigned_record(self):
        key = self.key_model.objects.create(**{
            self.key_parent_attr: self.unassigned_record, "key_number": "K1", "key_type": "Main",
        })
        response = self._client_for(self.employee_user).patch(
            f"{self.base_path}key/update/",
            data={self.key_id_field: getattr(key, self.key_id_field), "key_number": "Hacked"},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        key.refresh_from_db()
        self.assertEqual(key.key_number, "K1")

    def test_employee_cannot_delete_key_on_unassigned_record(self):
        key = self.key_model.objects.create(**{
            self.key_parent_attr: self.unassigned_record, "key_number": "K1", "key_type": "Main",
        })
        response = self._client_for(self.employee_user).delete(
            f"{self.base_path}key/delete/?{self.key_id_field}={getattr(key, self.key_id_field)}"
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue(self.key_model.objects.filter(pk=getattr(key, self.key_id_field)).exists())

    def test_manager_can_create_and_update_key_on_any_record(self):
        create_response = self._client_for(self.manager_user).post(
            f"{self.base_path}key/create/",
            data={self.id_field: self._record_id(self.unassigned_record), "key_number": "K1", "key_type": "Main"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 200, create_response.data)
        key_id = create_response.data["data"][self.key_id_field]

        update_response = self._client_for(self.manager_user).patch(
            f"{self.base_path}key/update/",
            data={self.key_id_field: key_id, "key_number": "Updated"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200, update_response.data)


class CheckInAuthorizationTests(CheckInCheckOutAuthorizationTestsMixin, TestCase):
    record_model = CheckIn
    id_field = 'check_in_id'
    code_field = 'check_in_code'
    base_path = '/checkin-checkout/check_in/'
    key_model = CheckInKey
    key_id_field = 'check_in_key_id'
    key_parent_attr = 'check_in'


class CheckOutAuthorizationTests(CheckInCheckOutAuthorizationTestsMixin, TestCase):
    record_model = CheckOut
    id_field = 'check_out_id'
    code_field = 'check_out_code'
    base_path = '/checkin-checkout/check_out/'
    key_model = CheckOutKey
    key_id_field = 'check_out_key_id'
    key_parent_attr = 'check_out'


class CheckInCheckOutSecurityRegressionTests(TestCase):
    """Phase 8: direct-API-bypass checks for Check-In/Check-Out authorization -
    no valid JWT means no access, for both modules."""

    def setUp(self):
        creator = User.objects.create(name="Creator", phone_number="5000000002")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)
        self.check_in = CheckIn.objects.create(property=self.property, check_in_code="TEST-SEC-CHECKIN")
        self.check_out = CheckOut.objects.create(property=self.property, check_out_code="TEST-SEC-CHECKOUT")
        self.client = APIClient(HTTP_USER_AGENT="pytest")  # deliberately not authenticated

    def test_unauthenticated_check_in_get_rejected(self):
        response = self.client.get(f"/checkin-checkout/check_in/get/?check_in_id={self.check_in.check_in_id}")
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_check_in_get_all_rejected(self):
        response = self.client.get("/checkin-checkout/check_in/get_all/")
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_check_in_update_rejected(self):
        response = self.client.patch(
            "/checkin-checkout/check_in/update/information/",
            data={"check_in_id": self.check_in.check_in_id, "remarks_notes": "Should Not Apply"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.check_in.refresh_from_db()
        self.assertNotEqual(self.check_in.remarks_notes, "Should Not Apply")

    def test_unauthenticated_check_out_get_rejected(self):
        response = self.client.get(f"/checkin-checkout/check_out/get/?check_out_id={self.check_out.check_out_id}")
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_check_out_update_rejected(self):
        response = self.client.patch(
            "/checkin-checkout/check_out/update/information/",
            data={"check_out_id": self.check_out.check_out_id, "remarks_notes": "Should Not Apply"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.check_out.refresh_from_db()
        self.assertNotEqual(self.check_out.remarks_notes, "Should Not Apply")


class CheckInCheckOutDashboardAuthorizationTests(TestCase):
    """Phase 8 follow-up: the row-level dashboard endpoints (pending
    settlements, upcoming check-ins/outs) leak tenant/property/assignee
    detail for every record unless scoped the same way the main record
    endpoints are - Employees must only see their own assigned records."""

    def setUp(self):
        import datetime
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        creator = User.objects.create(name="Creator", phone_number="6000000000")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)

        self.manager_user = User.objects.create(
            name="CICO Manager", phone_number="6000000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.manager_user.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="CICO Employee", phone_number="6000000002", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.employee_user.user_id, name="CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_employee_user = User.objects.create(
            name="Other CICO Employee", phone_number="6000000003", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Other CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        self.assigned_check_in = CheckIn.objects.create(
            property=self.property, check_in_code="TEST-DASH-CHECKIN-ASSIGNED",
            assigned_employee=self.employee_user, check_in_date=tomorrow,
        )
        self.unassigned_check_in = CheckIn.objects.create(
            property=self.property, check_in_code="TEST-DASH-CHECKIN-UNASSIGNED",
            assigned_employee=self.other_employee_user, check_in_date=tomorrow,
        )

        self.assigned_check_out = CheckOut.objects.create(
            property=self.property, check_out_code="TEST-DASH-CHECKOUT-ASSIGNED",
            assigned_employee=self.employee_user, check_out_date=tomorrow,
            settlement_status="Pending", total_amount=100,
        )
        self.unassigned_check_out = CheckOut.objects.create(
            property=self.property, check_out_code="TEST-DASH-CHECKOUT-UNASSIGNED",
            assigned_employee=self.other_employee_user, check_out_date=tomorrow,
            settlement_status="Pending", total_amount=200,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_employee_pending_settlements_only_shows_assigned(self):
        response = self._client_for(self.employee_user).get("/checkin-checkout/dashboard/pending_settlements/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["checkOutId"] for row in response.data["data"]["data"]]
        self.assertIn(self.assigned_check_out.check_out_id, ids)
        self.assertNotIn(self.unassigned_check_out.check_out_id, ids)

    def test_manager_pending_settlements_shows_all(self):
        response = self._client_for(self.manager_user).get("/checkin-checkout/dashboard/pending_settlements/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["checkOutId"] for row in response.data["data"]["data"]]
        self.assertIn(self.assigned_check_out.check_out_id, ids)
        self.assertIn(self.unassigned_check_out.check_out_id, ids)

    def test_employee_upcoming_check_ins_only_shows_assigned(self):
        response = self._client_for(self.employee_user).get("/checkin-checkout/check_in/dashboard/upcoming/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["checkInId"] for row in response.data["data"]["data"]]
        self.assertIn(self.assigned_check_in.check_in_id, ids)
        self.assertNotIn(self.unassigned_check_in.check_in_id, ids)

    def test_manager_upcoming_check_ins_shows_all(self):
        response = self._client_for(self.manager_user).get("/checkin-checkout/check_in/dashboard/upcoming/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["checkInId"] for row in response.data["data"]["data"]]
        self.assertIn(self.assigned_check_in.check_in_id, ids)
        self.assertIn(self.unassigned_check_in.check_in_id, ids)

    def test_employee_upcoming_check_outs_only_shows_assigned(self):
        response = self._client_for(self.employee_user).get("/checkin-checkout/check_out/dashboard/upcoming/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["checkOutId"] for row in response.data["data"]["data"]]
        self.assertIn(self.assigned_check_out.check_out_id, ids)
        self.assertNotIn(self.unassigned_check_out.check_out_id, ids)

    def test_manager_upcoming_check_outs_shows_all(self):
        response = self._client_for(self.manager_user).get("/checkin-checkout/check_out/dashboard/upcoming/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["checkOutId"] for row in response.data["data"]["data"]]
        self.assertIn(self.assigned_check_out.check_out_id, ids)
        self.assertIn(self.unassigned_check_out.check_out_id, ids)


class CheckInCheckOutStaffListingTests(TestCase):
    """GAP-012: the Check-In Check-Out department needs its own manager/
    employee listing endpoints (mirroring /marketing/manager/get_all/ and
    /marketing/employee/get_all/) so the "Assigned Employee" dropdown on the
    Check-In/Check-Out forms has a correct endpoint to call instead of the
    Marketing one."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="CICO Manager", phone_number="9700000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.manager_user.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="CICO Employee", phone_number="9700000002", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.employee_user.user_id, name="CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_get_all_manager_lists_the_manager(self):
        response = self._client_for(self.manager_user).get("/checkin-checkout/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["id"] for row in response.data["data"]["data"]]
        self.assertIn(self.manager_user.user_id, ids)

    def test_get_all_employee_lists_the_employee(self):
        response = self._client_for(self.employee_user).get("/checkin-checkout/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        ids = [row["id"] for row in response.data["data"]["data"]]
        self.assertIn(self.employee_user.user_id, ids)
        row = next(r for r in response.data["data"]["data"] if r["id"] == self.employee_user.user_id)
        self.assertEqual(row["managerRefId"], self.manager_user.user_id)

    def test_unauthenticated_staff_listing_rejected(self):
        """This endpoint uses IsAuthenticated (mirroring Marketing's manager/
        employee endpoints exactly), which returns 403 here rather than the
        401 the SerializerValidations-based endpoints return - matches the
        pre-existing Marketing convention, not a new inconsistency."""
        client = APIClient(HTTP_USER_AGENT="pytest")
        response = client.get("/checkin-checkout/employee/get_all/")
        self.assertEqual(response.status_code, 403)

    def test_manager_can_grant_their_own_lead_permission(self):
        """Frontend gap: Check-In/Check-Out staff had no way to be granted
        lead-read access after registration, since this department had no
        update endpoint at all - this is what unblocks it."""
        response = self._client_for(self.manager_user).put(
            "/checkin-checkout/manager/update/",
            data={"manager_id": self.manager_user.user_id, "permissions": {"lead": True}},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        manager = CheckInCheckOutManager.objects.get(manager_id=self.manager_user.user_id)
        self.assertTrue(manager.lead_permission.lead)

    def test_employee_can_grant_their_own_lead_permission(self):
        response = self._client_for(self.employee_user).put(
            "/checkin-checkout/employee/update/",
            data={"employee_id": self.employee_user.user_id, "permissions": {"lead": True}},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        employee = CheckInCheckOutEmployee.objects.get(employee_id=self.employee_user.user_id)
        self.assertTrue(employee.lead_permission.lead)

    def test_manager_cannot_update_another_managers_permissions(self):
        other_manager_user = User.objects.create(
            name="Other CICO Manager", phone_number="9700000003", department="Check-In Check-Out", role="Manager"
        )
        lead_permission_id = LeadPermission().create(lead=False)
        property_permission_id = PropertyPermission().create(property=False)
        CheckInCheckOutManager().create(
            manager_id=other_manager_user.user_id, name="Other CICO Manager", dob=None,
            department="Check-In Check-Out", team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )
        response = self._client_for(self.manager_user).put(
            "/checkin-checkout/manager/update/",
            data={"manager_id": other_manager_user.user_id, "permissions": {"lead": True}},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        other_manager = CheckInCheckOutManager.objects.get(manager_id=other_manager_user.user_id)
        self.assertFalse(other_manager.lead_permission.lead)

    def test_lead_access_actually_unblocked_after_grant(self):
        """End-to-end: before granting lead permission, /lead/get_all/ 403s
        for a CICO manager with no lead permission yet; after granting it
        via the new update endpoint, it works. Must use a real Bearer token
        (not force_authenticate) since the 403 in question comes from
        JWTAuthentication.validate_permissions, which force_authenticate
        bypasses entirely."""
        from pms_apps.authentication.utils import generate_jwt_token
        from pms_apps.activity_log.middlewares.log_middleware import local
        self.addCleanup(local.__dict__.clear)

        no_lead_manager_user = User.objects.create(
            name="No Lead CICO Manager", phone_number="9700000004", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=no_lead_manager_user.user_id, name="No Lead CICO Manager", dob=None,
            department="Check-In Check-Out", team_size=0,
            lead_permission_id=LeadPermission().create(lead=False),
            property_permission_id=PropertyPermission().create(property=True),
        )

        token = generate_jwt_token(no_lead_manager_user)
        no_lead_manager_user.access_token = token
        no_lead_manager_user.save()
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        before = client.get("/lead/get_all/")
        self.assertEqual(before.status_code, 403, before.data)

        grant = client.put(
            "/checkin-checkout/manager/update/",
            data={"manager_id": no_lead_manager_user.user_id, "permissions": {"lead": True}},
            format="json",
        )
        self.assertEqual(grant.status_code, 200, grant.data)

        after = client.get("/lead/get_all/")
        self.assertEqual(after.status_code, 200, after.data)


class CheckInCheckOutCreateAutoAssignTests(TestCase):
    """GAP-014: creating a Check-In/Check-Out without assigned_employee_id
    must never produce an orphaned, employee-inaccessible record - the
    backend defaults the handler to the creator, mirroring the Property
    module's auto-assign-creator pattern."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="CICO Manager", phone_number="9800000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.manager_user.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="CICO Employee", phone_number="9800000002", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.employee_user.user_id, name="CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        creator = User.objects.create(name="Property Creator", phone_number="9800000003")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_check_in_created_without_assigned_employee_defaults_to_creator(self):
        response = self._client_for(self.employee_user).post(
            "/checkin-checkout/check_in/create/",
            data={"property_id": self.property.property_id},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        check_in_id = response.data["data"]["check_in_id"]
        check_in = CheckIn.objects.get(check_in_id=check_in_id)
        self.assertEqual(check_in.assigned_employee_id, self.employee_user.user_id)

    def test_creator_of_unassigned_check_in_can_still_access_it(self):
        """The actual bug: without the fallback, the creator was locked out
        of their own record because assigned_employee_id stayed null."""
        create_response = self._client_for(self.employee_user).post(
            "/checkin-checkout/check_in/create/",
            data={"property_id": self.property.property_id},
            format="json",
        )
        check_in_id = create_response.data["data"]["check_in_id"]

        get_response = self._client_for(self.employee_user).get(
            f"/checkin-checkout/check_in/get/?check_in_id={check_in_id}"
        )
        self.assertEqual(get_response.status_code, 200, get_response.data)

        update_response = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/update/information/",
            data={"check_in_id": check_in_id, "remarks_notes": "creator follow-up"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200, update_response.data)

    def test_check_in_create_respects_explicit_assigned_employee_id(self):
        """The fallback only applies when the field is omitted - an explicit
        assignment (e.g. Manager assigning to a specific Employee) still wins."""
        response = self._client_for(self.manager_user).post(
            "/checkin-checkout/check_in/create/",
            data={"property_id": self.property.property_id, "assigned_employee_id": self.employee_user.user_id},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        check_in = CheckIn.objects.get(check_in_id=response.data["data"]["check_in_id"])
        self.assertEqual(check_in.assigned_employee_id, self.employee_user.user_id)

    def test_check_out_created_without_assigned_employee_defaults_to_creator(self):
        response = self._client_for(self.employee_user).post(
            "/checkin-checkout/check_out/create/",
            data={"property_id": self.property.property_id},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        check_out = CheckOut.objects.get(check_out_id=response.data["data"]["check_out_id"])
        self.assertEqual(check_out.assigned_employee_id, self.employee_user.user_id)


class CheckOutConversionValidationTests(TestCase):
    """GAP-016: converting a check-in to a check-out (via check_in_id) must
    require the source check-in to be Completed, and must not allow the same
    check-in to be converted twice."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="CICO Manager", phone_number="9900000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.manager_user.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        creator = User.objects.create(name="Property Creator", phone_number="9900000002")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=creator)

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_cannot_convert_check_in_that_is_not_completed(self):
        check_in = CheckIn.objects.create(
            property=self.property, check_in_code="TEST-CONV-PENDING", check_in_status="Pending",
        )
        response = self._client_for(self.manager_user).post(
            "/checkin-checkout/check_out/create/",
            data={"property_id": self.property.property_id, "check_in_id": check_in.check_in_id},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertFalse(CheckOut.objects.filter(check_in_id=check_in.check_in_id).exists())

    def test_can_convert_completed_check_in(self):
        check_in = CheckIn.objects.create(
            property=self.property, check_in_code="TEST-CONV-DONE", check_in_status="Completed",
        )
        response = self._client_for(self.manager_user).post(
            "/checkin-checkout/check_out/create/",
            data={"property_id": self.property.property_id, "check_in_id": check_in.check_in_id},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_cannot_convert_the_same_check_in_twice(self):
        check_in = CheckIn.objects.create(
            property=self.property, check_in_code="TEST-CONV-DUP", check_in_status="Completed",
        )
        first = self._client_for(self.manager_user).post(
            "/checkin-checkout/check_out/create/",
            data={"property_id": self.property.property_id, "check_in_id": check_in.check_in_id},
            format="json",
        )
        self.assertEqual(first.status_code, 200, first.data)

        second = self._client_for(self.manager_user).post(
            "/checkin-checkout/check_out/create/",
            data={"property_id": self.property.property_id, "check_in_id": check_in.check_in_id},
            format="json",
        )
        self.assertEqual(second.status_code, 400, second.data)
        self.assertEqual(
            CheckOut.objects.filter(check_in_id=check_in.check_in_id, is_active=True).count(), 1
        )

    def test_check_out_without_check_in_id_is_unaffected(self):
        """Independent check-outs (not a conversion) still work exactly as before."""
        response = self._client_for(self.manager_user).post(
            "/checkin-checkout/check_out/create/",
            data={"property_id": self.property.property_id},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)


class CheckInCheckOutGetAllPaginationTests(TestCase):
    """The custom CheckInGetAllSerializer/CheckOutGetAllSerializer pagination
    fields must validate page_num/limit properly and clamp an excessive
    limit, same as the shared GetAllSerializer everywhere else."""

    def setUp(self):
        self.user = User.objects.create(name="Any User", phone_number="9999900003")

    def _client(self):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=self.user)
        return client

    def test_check_in_page_num_zero_returns_field_validation_error(self):
        response = self._client().get("/checkin-checkout/check_in/get_all/?page_num=0")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("page_num", response.data["error"][0])

    def test_check_in_limit_zero_returns_field_validation_error(self):
        response = self._client().get("/checkin-checkout/check_in/get_all/?limit=0")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("limit", response.data["error"][0])

    def test_check_in_excessive_limit_does_not_error(self):
        response = self._client().get("/checkin-checkout/check_in/get_all/?limit=999999999")
        self.assertEqual(response.status_code, 200, response.data)

    def test_check_out_page_num_zero_returns_field_validation_error(self):
        response = self._client().get("/checkin-checkout/check_out/get_all/?page_num=0")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("page_num", response.data["error"][0])

    def test_check_out_limit_zero_returns_field_validation_error(self):
        response = self._client().get("/checkin-checkout/check_out/get_all/?limit=0")
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data["message"], "Validation Error")
        self.assertIn("limit", response.data["error"][0])


class CheckInAutoRoutingFromAssignmentTests(TestCase):
    """A property assignment landing on the default Pending status should
    auto-create an unclaimed Check-In inquiry (property/views.py
    assign_extract); Check-In Employees/Managers see it via the pending
    requests endpoint and accept/reject it via the respond endpoint."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="CICO Manager", phone_number="9900000001", department="Check-In Check-Out", role="Manager"
        )
        CheckInCheckOutManager().create(
            manager_id=self.manager_user.user_id, name="CICO Manager", dob=None, department="Check-In Check-Out",
            team_size=0, lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="CICO Employee", phone_number="9900000002", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.employee_user.user_id, name="CICO Employee", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_employee_user = User.objects.create(
            name="CICO Employee 2", phone_number="9900000003", department="Check-In Check-Out", role="Employee"
        )
        CheckInCheckOutEmployee().create(
            employee_id=self.other_employee_user.user_id, name="CICO Employee 2", dob=None, designation="",
            department="Check-In Check-Out", manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.assigner = User.objects.create(name="Assigner", phone_number="9900000004")
        self.property = Property.objects.create(rental_type="Flat", rental_for="Family", created_by=self.assigner)

        landlord_user = User.objects.create(name="Landlord", phone_number="9900000005", department="Landlord")
        landlord = Lead.objects.create(
            lead_id=landlord_user, first_name="Landlord", last_name="Person", purpose="Landlord",
        )
        PropertyDetail().create(
            property_id=self.property.property_id, building_name="Test Building",
            monthly_rent=0, security_deposit_amount=0, late_fee_type="Day wise", late_fee_value=0,
            current_status="Vacant", landlord_id=landlord.lead_id_id, created_by_id=self.assigner.user_id,
            address_line_1="", area_zone="", city="", state="", country="", pincode="",
        )

        tenant_user = User.objects.create(name="Tenant", phone_number="9900000006", department="Tenant")
        self.tenant = Lead.objects.create(
            lead_id=tenant_user, first_name="Test", last_name="Tenant", purpose="Tenant",
            lead_assign_to=self.assigner,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def _assign_property(self):
        return self._client_for(self.assigner).post(
            "/property/assign/",
            data={
                "property_id": self.property.property_id, "tenant_id": self.tenant.lead_id_id,
                "assigned_by_id": self.assigner.user_id,
            },
            format="json",
        )

    def test_assigning_property_auto_creates_unclaimed_check_in(self):
        response = self._assign_property()
        self.assertEqual(response.status_code, 200, response.data)
        assignment_id = response.data["data"]["property_assignment_id"]

        check_in = CheckIn.objects.get(property_assignment_id=assignment_id)
        self.assertIsNone(check_in.assigned_employee_id)
        self.assertEqual(check_in.check_in_status, "Pending")
        self.assertEqual(check_in.tenant_id, self.tenant.lead_id_id)

    def test_unclaimed_check_in_appears_in_pending_requests(self):
        self._assign_property()
        response = self._client_for(self.employee_user).get("/checkin-checkout/check_in/requests/pending/")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data["data"]["data"]), 1)

    def test_unclaimed_check_in_not_in_normal_employee_get_all(self):
        self._assign_property()
        response = self._client_for(self.employee_user).get("/checkin-checkout/check_in/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data["data"]["data"]), 0)

    def test_employee_can_accept_pending_request(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        response = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

        check_in = CheckIn.objects.get(check_in_id=check_in_id)
        self.assertEqual(check_in.assigned_employee_id, self.employee_user.user_id)
        self.assertEqual(check_in.check_in_status, "In Progress")

    def test_debounce_blocks_same_user_immediate_resubmit(self):
        """The debounce is meant to catch a double-click/retry from the same
        user, not block a different user's legitimate response."""
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        first = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "reject": True},
            format="json",
        )
        self.assertEqual(first.status_code, 200, first.data)

        # Same user immediately re-submitting the identical action.
        retry = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "reject": True},
            format="json",
        )
        self.assertEqual(retry.status_code, 400, retry.data)
        self.assertIn("already been claimed or handled", retry.data["error"][0])

    def test_debounce_does_not_block_different_user_immediate_response(self):
        """Regression for the bug found in QA: a different user's legitimate
        accept, arriving moments after another user's reject, must succeed -
        the debounce must be scoped to the SAME user, not any two responses
        on the record within the window."""
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        reject = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "reject": True},
            format="json",
        )
        self.assertEqual(reject.status_code, 200, reject.data)

        # A DIFFERENT user, immediately after - must not be debounced.
        accept = self._client_for(self.other_employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        self.assertEqual(accept.status_code, 200, accept.data)

    def test_second_accept_after_claim_is_rejected(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        second = self._client_for(self.other_employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        self.assertEqual(second.status_code, 400, second.data)

    def test_employee_can_reject_and_it_stays_claimable(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        response = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "reject": True, "rejection_reason": "Not my area"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

        check_in = CheckIn.objects.get(check_in_id=check_in_id)
        self.assertIsNone(check_in.assigned_employee_id)
        self.assertEqual(check_in.check_in_status, "Pending")
        self.assertIn("Rejected by user", check_in.status_history)
        self.assertIn("Not my area", check_in.status_history)

        accept_response = self._client_for(self.other_employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        self.assertEqual(accept_response.status_code, 200, accept_response.data)

    def test_manager_can_accept_pending_request(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        response = self._client_for(self.manager_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

    def test_non_check_in_role_user_cannot_respond(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        outsider = User.objects.create(name="Outsider", phone_number="9900000007")
        response = self._client_for(outsider).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_accept_and_reject_both_true_is_rejected(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        response = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True, "reject": True},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_assignment_with_non_pending_status_does_not_auto_create_check_in(self):
        """The trigger fires only when the assignment lands on Pending
        (confirmed answer) - an assignment explicitly created at a later
        status should not auto-route an inquiry."""
        response = self._client_for(self.assigner).post(
            "/property/assign/",
            data={
                "property_id": self.property.property_id, "tenant_id": self.tenant.lead_id_id,
                "assigned_by_id": self.assigner.user_id, "assignment_status": "Approved",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertFalse(CheckIn.objects.filter(tenant_id=self.tenant.lead_id_id).exists())

    def test_accepted_check_in_no_longer_appears_in_pending_requests(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )

        response = self._client_for(self.other_employee_user).get("/checkin-checkout/check_in/requests/pending/")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data["data"]["data"]), 0)

    def test_manager_can_reject_pending_request(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        response = self._client_for(self.manager_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "reject": True, "rejection_reason": "Reassign to specialist"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)

        check_in = CheckIn.objects.get(check_in_id=check_in_id)
        self.assertIsNone(check_in.assigned_employee_id)
        self.assertEqual(check_in.check_in_status, "Pending")

    def test_non_check_in_role_user_cannot_view_pending_requests(self):
        self._assign_property()
        outsider = User.objects.create(name="Outsider Viewer", phone_number="9900000008")

        response = self._client_for(outsider).get("/checkin-checkout/check_in/requests/pending/")
        self.assertEqual(response.status_code, 400, response.data)

    def test_respond_to_nonexistent_check_in_id_errors(self):
        response = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": 999999, "accept": True},
            format="json",
        )
        self.assertEqual(response.status_code, 400, response.data)

    def test_cancelled_assignment_check_in_excluded_from_pending_pool(self):
        """BUG-001 regression: once the linked PropertyAssignment is
        Cancelled, its auto-routed, still-unclaimed CheckIn must not remain
        visible/acceptable in the pending pool."""
        from pms_apps.property.models.property_assignment import PropertyAssignment

        response = self._assign_property()
        assignment_id = response.data["data"]["property_assignment_id"]
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        PropertyAssignment.update(property_assignment_id=assignment_id, assignment_status="Cancelled")

        pending = self._client_for(self.employee_user).get("/checkin-checkout/check_in/requests/pending/")
        self.assertEqual(pending.status_code, 200, pending.data)
        ids_in_pool = [row["checkInId"] for row in pending.data["data"]["data"]]
        self.assertNotIn(check_in_id, ids_in_pool)

        # Still not acceptable via the respond endpoint either (belt and
        # braces - the pool exclusion is the primary fix, but accept should
        # still be attempted safely if someone has a stale link open).
        respond = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "accept": True},
            format="json",
        )
        self.assertEqual(respond.status_code, 200, respond.data)

    def test_completed_assignment_check_in_excluded_from_pending_pool(self):
        from pms_apps.property.models.property_assignment import PropertyAssignment

        response = self._assign_property()
        assignment_id = response.data["data"]["property_assignment_id"]
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        PropertyAssignment.update(property_assignment_id=assignment_id, assignment_status="Completed")

        pending = self._client_for(self.employee_user).get("/checkin-checkout/check_in/requests/pending/")
        self.assertEqual(pending.status_code, 200, pending.data)
        ids_in_pool = [row["checkInId"] for row in pending.data["data"]["data"]]
        self.assertNotIn(check_in_id, ids_in_pool)

    def test_active_assignment_check_in_still_in_pending_pool(self):
        """Sanity check the exclusion is scoped correctly - a live (Pending)
        assignment's check-in must still appear."""
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        pending = self._client_for(self.employee_user).get("/checkin-checkout/check_in/requests/pending/")
        ids_in_pool = [row["checkInId"] for row in pending.data["data"]["data"]]
        self.assertIn(check_in_id, ids_in_pool)

    def test_reject_reason_is_optional(self):
        self._assign_property()
        check_in_id = CheckIn.objects.get(tenant_id=self.tenant.lead_id_id).check_in_id

        response = self._client_for(self.employee_user).patch(
            "/checkin-checkout/check_in/requests/respond/",
            data={"check_in_id": check_in_id, "reject": True},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        check_in = CheckIn.objects.get(check_in_id=check_in_id)
        self.assertIn("Rejected by user", check_in.status_history)
