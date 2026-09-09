from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.maintenance.models.maintenance_manager import MaintenanceManager
from pms_apps.maintenance.models.maintenance_employee import MaintenanceEmployee
from pms_apps.maintenance.models.maintenance_technician import MaintenanceTechnician
from pms_apps.common.models.permissions import PropertyPermission


class MaintenanceGetAllScopingTests(TestCase):
    """Issue 4: manager/get_all/, employee/get_all/ and technician/get_all/
    must not leak data across teams - a Manager only sees their own team, an
    Employee only sees themself (and the manager they report to), and a
    Technician (no manager link) only ever sees themself."""

    def setUp(self):
        property_permission_id = PropertyPermission().create(property=True)

        self.manager_user = User.objects.create(
            name="Maintenance Manager", phone_number="1800000001", department="Maintenance", role="Manager"
        )
        MaintenanceManager().create(
            manager_id=self.manager_user.user_id, name="Maintenance Manager", dob=None, specialization="",
            team_size=0, years_of_experience=0, property_permission_id=property_permission_id,
        )

        self.employee_user = User.objects.create(
            name="Maintenance Employee", phone_number="1800000002", department="Maintenance", role="Employee"
        )
        MaintenanceEmployee().create(
            employee_id=self.employee_user.user_id, name="Maintenance Employee", dob=None, designation="",
            specialization="", assigned_tasks=0, manager_ref=self.manager_user.user_id,
            property_permission_id=property_permission_id,
        )

        self.other_manager_user = User.objects.create(
            name="Maintenance Manager Two", phone_number="1800000003", department="Maintenance", role="Manager"
        )
        MaintenanceManager().create(
            manager_id=self.other_manager_user.user_id, name="Maintenance Manager Two", dob=None, specialization="",
            team_size=0, years_of_experience=0, property_permission_id=property_permission_id,
        )

        self.other_employee_user = User.objects.create(
            name="Maintenance Employee Two", phone_number="1800000004", department="Maintenance", role="Employee"
        )
        MaintenanceEmployee().create(
            employee_id=self.other_employee_user.user_id, name="Maintenance Employee Two", dob=None, designation="",
            specialization="", assigned_tasks=0, manager_ref=self.other_manager_user.user_id,
            property_permission_id=property_permission_id,
        )

        self.technician_user = User.objects.create(
            name="Maintenance Technician", phone_number="1800000005", department="Maintenance", role="Technician"
        )
        MaintenanceTechnician().create(
            technician_id=self.technician_user.user_id, name="Maintenance Technician", dob=None,
            skill_type="", years_of_experience=0, assigned_jobs=0, property_permission_id=property_permission_id,
        )

        self.other_technician_user = User.objects.create(
            name="Maintenance Technician Two", phone_number="1800000006", department="Maintenance", role="Technician"
        )
        MaintenanceTechnician().create(
            technician_id=self.other_technician_user.user_id, name="Maintenance Technician Two", dob=None,
            skill_type="", years_of_experience=0, assigned_jobs=0, property_permission_id=property_permission_id,
        )

    def _client_for(self, user):
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.force_authenticate(user=user)
        return client

    def test_manager_get_all_manager_returns_self_only(self):
        response = self._client_for(self.manager_user).get("/maintenance/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])

    def test_manager_get_all_employee_returns_own_team_only(self):
        response = self._client_for(self.manager_user).get("/maintenance/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])

    def test_employee_get_all_employee_returns_self_only(self):
        response = self._client_for(self.employee_user).get("/maintenance/employee/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        employee_ids = [row["employeeId"] for row in response.data["data"]["data"]]
        self.assertEqual(employee_ids, [self.employee_user.user_id])
        self.assertNotIn(self.other_employee_user.user_id, employee_ids)

    def test_employee_get_all_manager_returns_own_manager_only(self):
        response = self._client_for(self.employee_user).get("/maintenance/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        manager_ids = [row["managerId"] for row in response.data["data"]["data"]]
        self.assertEqual(manager_ids, [self.manager_user.user_id])
        self.assertNotIn(self.other_manager_user.user_id, manager_ids)

    def test_technician_get_all_returns_self_only(self):
        response = self._client_for(self.technician_user).get("/maintenance/technician/get_all/")
        self.assertEqual(response.status_code, 200, response.data)
        technician_ids = [row["technicianId"] for row in response.data["data"]["data"]]
        self.assertEqual(technician_ids, [self.technician_user.user_id])
        self.assertNotIn(self.other_technician_user.user_id, technician_ids)
