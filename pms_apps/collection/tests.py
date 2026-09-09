from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.collection.models.collection_manager import CollectionManager
from pms_apps.collection.models.collection_employee import CollectionEmployee


class CollectionGetAllScopingTests(TestCase):
    """Issue 4: manager/get_all/ and employee/get_all/ must not leak data
    across teams - a Manager only sees their own team, an Employee only
    sees themself (and the manager they report to)."""

    def setUp(self):
        self.manager_user = User.objects.create(
            name="Collection Manager", phone_number="1600000001", department="Collection", role="Manager"
        )
        CollectionManager().create(
            manager_id=self.manager_user.user_id, name="Collection Manager", dob=None, department="Collection",
            total_collections=0, overdue_accounts_managed=0, team_size=0,
        )

        self.employee_user = User.objects.create(
            name="Collection Employee", phone_number="1600000002", department="Collection", role="Employee"
        )
        CollectionEmployee().create(
            employee_id=self.employee_user.user_id, name="Collection Employee", dob=None, designation="",
            region="", collections_made=0, overdue_accounts_handled=0, manager_ref=self.manager_user.user_id,
        )

        self.other_manager_user = User.objects.create(
            name="Collection Manager Two", phone_number="1600000003", department="Collection", role="Manager"
        )
        CollectionManager().create(
            manager_id=self.other_manager_user.user_id, name="Collection Manager Two", dob=None, department="Collection",
            total_collections=0, overdue_accounts_managed=0, team_size=0,
        )

        self.other_employee_user = User.objects.create(
            name="Collection Employee Two", phone_number="1600000004", department="Collection", role="Employee"
        )
        CollectionEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Collection Employee Two", dob=None, designation="",
            region="", collections_made=0, overdue_accounts_handled=0, manager_ref=self.other_manager_user.user_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_get_all_manager_returns_self_only(self):
        response = self._client_for(self.manager_user).get("/collection/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])

    def test_manager_get_all_employee_returns_own_team_only(self):
        response = self._client_for(self.manager_user).get("/collection/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])

    def test_employee_get_all_employee_returns_self_only(self):
        response = self._client_for(self.employee_user).get("/collection/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])
        self.assertNotIn(self.other_employee_user.user_id, employee_ids)

    def test_employee_get_all_manager_returns_own_manager_only(self):
        response = self._client_for(self.employee_user).get("/collection/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)
