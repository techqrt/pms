from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.IT.models.IT_manager import ITManager
from pms_apps.IT.models.IT_employee import ITEmployee
from pms_apps.IT.models.IT_technician import ITTechnician


class ITGetAllScopingTests(TestCase):
    """Issue 4: manager/get_all/, employee/get_all/ and technician/get_all/
    must not leak data across teams - a Manager only sees their own team, an
    Employee only sees themself (and the manager they report to), and a
    Technician (no manager link) only ever sees themself."""

    def setUp(self):
        self.manager_user = User.objects.create(
            name="IT Manager", phone_number="1700000001", department="IT", role="Manager"
        )
        ITManager().create(
            manager_id=self.manager_user.user_id, name="IT Manager", dob=None, department="IT",
            projects_managed=0, systems_overseen=0, team_size=0,
        )

        self.employee_user = User.objects.create(
            name="IT Employee", phone_number="1700000002", department="IT", role="Employee"
        )
        ITEmployee().create(
            employee_id=self.employee_user.user_id, name="IT Employee", dob=None, role_title="",
            tickets_resolved=0, projects_assigned=0, specialization="", manager_ref=self.manager_user.user_id,
        )

        self.other_manager_user = User.objects.create(
            name="IT Manager Two", phone_number="1700000003", department="IT", role="Manager"
        )
        ITManager().create(
            manager_id=self.other_manager_user.user_id, name="IT Manager Two", dob=None, department="IT",
            projects_managed=0, systems_overseen=0, team_size=0,
        )

        self.other_employee_user = User.objects.create(
            name="IT Employee Two", phone_number="1700000004", department="IT", role="Employee"
        )
        ITEmployee().create(
            employee_id=self.other_employee_user.user_id, name="IT Employee Two", dob=None, role_title="",
            tickets_resolved=0, projects_assigned=0, specialization="", manager_ref=self.other_manager_user.user_id,
        )

        self.technician_user = User.objects.create(
            name="IT Technician", phone_number="1700000005", department="IT", role="Technician"
        )
        ITTechnician().create(
            technician_id=self.technician_user.user_id, name="IT Technician", dob=None,
            skill_area="", tickets_closed=0, years_of_experience=0,
        )

        self.other_technician_user = User.objects.create(
            name="IT Technician Two", phone_number="1700000006", department="IT", role="Technician"
        )
        ITTechnician().create(
            technician_id=self.other_technician_user.user_id, name="IT Technician Two", dob=None,
            skill_area="", tickets_closed=0, years_of_experience=0,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_get_all_manager_returns_self_only(self):
        response = self._client_for(self.manager_user).get("/it/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])

    def test_manager_get_all_employee_returns_own_team_only(self):
        response = self._client_for(self.manager_user).get("/it/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])

    def test_employee_get_all_employee_returns_self_only(self):
        response = self._client_for(self.employee_user).get("/it/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])
        self.assertNotIn(self.other_employee_user.user_id, employee_ids)

    def test_employee_get_all_manager_returns_own_manager_only(self):
        response = self._client_for(self.employee_user).get("/it/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)

    def test_technician_get_all_returns_self_only(self):
        response = self._client_for(self.technician_user).get("/it/technician/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        technician_ids = [row["technicianId"] for row in response.data["data"]["data"]]
        self.assertEqual(technician_ids, [self.technician_user.user_id])
        self.assertNotIn(self.other_technician_user.user_id, technician_ids)
