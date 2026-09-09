from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.legal.models.legal_manager import LegalManager
from pms_apps.legal.models.legal_employee import LegalEmployee


class LegalGetAllScopingTests(TestCase):
    """Issue 4: manager/get_all/ and employee/get_all/ must not leak data
    across teams - a Manager only sees their own team, an Employee only
    sees themself (and the manager they report to)."""

    def setUp(self):
        self.manager_user = User.objects.create(
            name="Legal Manager", phone_number="1400000001", department="Legal", role="Manager"
        )
        LegalManager().create(
            manager_id=self.manager_user.user_id, name="Legal Manager", dob=None, department="Legal",
            total_cases_handled=0, open_cases=0, closed_cases=0, team_size=0,
        )

        self.employee_user = User.objects.create(
            name="Legal Employee", phone_number="1400000002", department="Legal", role="Employee"
        )
        LegalEmployee().create(
            employee_id=self.employee_user.user_id, name="Legal Employee", dob=None, designation="",
            active_cases=0, case_specialization="", manager_ref=self.manager_user.user_id,
        )

        self.other_manager_user = User.objects.create(
            name="Legal Manager Two", phone_number="1400000003", department="Legal", role="Manager"
        )
        LegalManager().create(
            manager_id=self.other_manager_user.user_id, name="Legal Manager Two", dob=None, department="Legal",
            total_cases_handled=0, open_cases=0, closed_cases=0, team_size=0,
        )

        self.other_employee_user = User.objects.create(
            name="Legal Employee Two", phone_number="1400000004", department="Legal", role="Employee"
        )
        LegalEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Legal Employee Two", dob=None, designation="",
            active_cases=0, case_specialization="", manager_ref=self.other_manager_user.user_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_get_all_manager_returns_self_only(self):
        response = self._client_for(self.manager_user).get("/legal/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])

    def test_manager_get_all_employee_returns_own_team_only(self):
        response = self._client_for(self.manager_user).get("/legal/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])

    def test_employee_get_all_employee_returns_self_only(self):
        response = self._client_for(self.employee_user).get("/legal/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])
        self.assertNotIn(self.other_employee_user.user_id, employee_ids)

    def test_employee_get_all_manager_returns_own_manager_only(self):
        response = self._client_for(self.employee_user).get("/legal/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)
