from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.reception.models.reception_manager import ReceptionManager
from pms_apps.reception.models.reception_employee import ReceptionEmployee


class ReceptionGetAllScopingTests(TestCase):
    """Issue 4: manager/get_all/ and employee/get_all/ must not leak data
    across teams - a Manager only sees their own team, an Employee only
    sees themself (and the manager they report to)."""

    def setUp(self):
        self.manager_user = User.objects.create(
            name="Reception Manager", phone_number="1500000001", department="Reception", role="Manager"
        )
        ReceptionManager().create(
            manager_id=self.manager_user.user_id, name="Reception Manager", dob=None, department="Reception",
            team_size=0, front_desk_count=0,
        )

        self.employee_user = User.objects.create(
            name="Reception Employee", phone_number="1500000002", department="Reception", role="Employee"
        )
        ReceptionEmployee().create(
            employee_id=self.employee_user.user_id, name="Reception Employee", dob=None, shift="", desk_number="",
            calls_handled=0, visitors_logged=0, manager_ref=self.manager_user.user_id,
        )

        self.other_manager_user = User.objects.create(
            name="Reception Manager Two", phone_number="1500000003", department="Reception", role="Manager"
        )
        ReceptionManager().create(
            manager_id=self.other_manager_user.user_id, name="Reception Manager Two", dob=None, department="Reception",
            team_size=0, front_desk_count=0,
        )

        self.other_employee_user = User.objects.create(
            name="Reception Employee Two", phone_number="1500000004", department="Reception", role="Employee"
        )
        ReceptionEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Reception Employee Two", dob=None, shift="", desk_number="",
            calls_handled=0, visitors_logged=0, manager_ref=self.other_manager_user.user_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_get_all_manager_returns_self_only(self):
        response = self._client_for(self.manager_user).get("/reception/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])

    def test_manager_get_all_employee_returns_own_team_only(self):
        response = self._client_for(self.manager_user).get("/reception/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])

    def test_employee_get_all_employee_returns_self_only(self):
        response = self._client_for(self.employee_user).get("/reception/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])
        self.assertNotIn(self.other_employee_user.user_id, employee_ids)

    def test_employee_get_all_manager_returns_own_manager_only(self):
        response = self._client_for(self.employee_user).get("/reception/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)
