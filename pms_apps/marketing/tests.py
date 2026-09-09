from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.marketing.models.marketing_employee import MarketingEmployee
from pms_apps.common.models.permissions import LeadPermission, PropertyPermission


class MarketingManagerGetAllScopingTests(TestCase):
    """Issue 3: manager/get_all/ must return the authenticated Manager's own
    data plus their Employees' data, and never another Manager's team.
    Issue 4: an Employee hitting this endpoint must only see their own
    Manager, never another team."""

    def setUp(self):
        lead_permission_id = LeadPermission().create(lead=True)
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Manager One", phone_number="1200000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.manager_user.user_id, name="Manager One", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="Employee One", phone_number="1200000002", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.employee_user.user_id, name="Employee One", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_manager_user = User.objects.create(
            name="Manager Two", phone_number="1200000003", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=self.other_manager_user.user_id, name="Manager Two", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.other_employee_user = User.objects.create(
            name="Employee Two", phone_number="1200000004", department="Marketing", role="Employee"
        )
        MarketingEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Employee Two", dob=None,
            designation="", department="Marketing", campaigns_assigned=0, leads_generated=0,
            manager_ref=self.other_manager_user.user_id,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_get_all_returns_own_data_and_own_employees_only(self):
        response = self._client_for(self.manager_user).get("/marketing/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        rows = response.data["data"]["data"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["managerId"], self.manager_user.user_id)

        employee_ids = [e["employeeId"] for e in rows[0]["employees"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])

    def test_manager_get_all_excludes_other_managers(self):
        response = self._client_for(self.manager_user).get("/marketing/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)

    def test_employee_get_all_returns_only_their_own_manager(self):
        response = self._client_for(self.employee_user).get("/marketing/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        rows = response.data["data"]["data"]
        manager_ids = [row["managerId"] for row in rows]
        self.assertEqual(manager_ids, [self.manager_user.user_id])
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)


class MarketingManagerUpdatePasswordTests(TestCase):
    """PUT /marketing/manager/update/ also supports changing the manager's
    own password via old_password/new_password (no dedicated endpoint)."""

    def setUp(self):
        self.user = User.objects.create(name="Manager One", phone_number="1112223333")
        self.user.set_password("123456789")
        self.user.save()
        lead_permission_id = LeadPermission().create(lead=False)
        property_permission_id = PropertyPermission().create(property=False)
        MarketingManager().create(
            manager_id=self.user.user_id, name="Manager One", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=lead_permission_id, property_permission_id=property_permission_id,
        )

        self.client = APIClient(HTTP_USER_AGENT="pytest")
        self.client.force_authenticate(user=self.user)

    def base_payload(self):
        return {
            "manager_id": self.user.user_id,
            "name": "Manager One",
            "dob": None,
            "department": "Marketing",
        }

    def test_password_change_with_correct_old_password_succeeds(self):
        payload = self.base_payload()
        payload["old_password"] = "123456789"
        payload["new_password"] = "12341234"
        response = self.client.put("/marketing/manager/update/", data=payload, format="json")
        self.assertEqual(response.status_code, 200, response.data)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("12341234"))
        self.assertFalse(self.user.check_password("123456789"))

    def test_password_change_with_wrong_old_password_fails(self):
        payload = self.base_payload()
        payload["old_password"] = "wrong-password"
        payload["new_password"] = "12341234"
        response = self.client.put("/marketing/manager/update/", data=payload, format="json")
        self.assertEqual(response.status_code, 400)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("123456789"))

    def test_update_without_password_fields_does_not_touch_password(self):
        response = self.client.put("/marketing/manager/update/", data=self.base_payload(), format="json")
        self.assertEqual(response.status_code, 200, response.data)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("123456789"))

    def test_only_new_password_without_old_password_fails(self):
        payload = self.base_payload()
        payload["new_password"] = "12341234"
        response = self.client.put("/marketing/manager/update/", data=payload, format="json")
        self.assertEqual(response.status_code, 400)
