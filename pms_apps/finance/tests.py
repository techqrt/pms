from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.finance.models.finance_manager import FinanceManager
from pms_apps.finance.models.finance_employee import FinanceEmployee


class FinanceGetAllScopingTests(TestCase):
    """Issue 4: manager/get_all/ and employee/get_all/ must not leak data
    across teams - a Manager only sees their own team, an Employee only
    sees themself (and the manager they report to)."""

    def setUp(self):
        self.manager_user = User.objects.create(
            name="Finance Manager", phone_number="1300000001", department="Finance", role="Manager"
        )
        FinanceManager().create(
            manager_id=self.manager_user.user_id, name="Finance Manager", dob=None, department="Finance",
            total_budget_managed=0, reports_submitted=0, team_size=0,
        )

        self.employee_user = User.objects.create(
            name="Finance Employee", phone_number="1300000002", department="Finance", role="Employee"
        )
        FinanceEmployee().create(
            employee_id=self.employee_user.user_id, name="Finance Employee", dob=None, role_title="",
            invoices_processed=0, payments_verified=0, total_amount_handled=0,
            manager_ref=self.manager_user.user_id,
        )

        self.other_manager_user = User.objects.create(
            name="Finance Manager Two", phone_number="1300000003", department="Finance", role="Manager"
        )
        FinanceManager().create(
            manager_id=self.other_manager_user.user_id, name="Finance Manager Two", dob=None, department="Finance",
            total_budget_managed=0, reports_submitted=0, team_size=0,
        )

        self.other_employee_user = User.objects.create(
            name="Finance Employee Two", phone_number="1300000004", department="Finance", role="Employee"
        )
        FinanceEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Finance Employee Two", dob=None, role_title="",
            invoices_processed=0, payments_verified=0, total_amount_handled=0,
            manager_ref=self.other_manager_user.user_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_get_all_manager_returns_self_only(self):
        response = self._client_for(self.manager_user).get("/finance/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])

    def test_manager_get_all_employee_returns_own_team_only(self):
        response = self._client_for(self.manager_user).get("/finance/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])

    def test_employee_get_all_employee_returns_self_only(self):
        response = self._client_for(self.employee_user).get("/finance/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])
        self.assertNotIn(self.other_employee_user.user_id, employee_ids)

    def test_employee_get_all_manager_returns_own_manager_only(self):
        response = self._client_for(self.employee_user).get("/finance/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)
