from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.authentication.utils import generate_jwt_token


class RegistrationDefaultPermissionsTests(TestCase):
    """Every department's Manager/Employee/Technician (and Tenant/Landlord
    Lead) must be created with its own granted LeadPermission/
    PropertyPermission record at registration - previously these were left
    null, which silently denied cross-department access (e.g. Check-In
    Check-Out staff reading Lead records) with no way to fix it afterwards
    for departments with no update endpoint."""

    def _register(self, phone_number, role, module):
        client = APIClient(HTTP_USER_AGENT="pytest")
        response = client.post(
            "/auth/register/",
            data={"phone_number": phone_number, "role": role, "module": module},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        return User.objects.get(phone_number=phone_number)

    def test_check_in_check_out_manager_gets_lead_and_property_permission(self):
        from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager

        user = self._register("6700000001", "Manager", "Check-In Check-Out")
        manager = CheckInCheckOutManager.objects.get(manager_id=user)
        self.assertIsNotNone(manager.lead_permission)
        self.assertTrue(manager.lead_permission.lead)
        self.assertIsNotNone(manager.property_permission)
        self.assertTrue(manager.property_permission.property)

    def test_check_in_check_out_employee_gets_lead_and_property_permission(self):
        from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee

        user = self._register("6700000002", "Employee", "Check-In Check-Out")
        employee = CheckInCheckOutEmployee.objects.get(employee_id=user)
        self.assertIsNotNone(employee.lead_permission)
        self.assertTrue(employee.lead_permission.lead)
        self.assertIsNotNone(employee.property_permission)
        self.assertTrue(employee.property_permission.property)

    def test_marketing_manager_gets_lead_and_property_permission(self):
        from pms_apps.marketing.models.marketing_manager import MarketingManager

        user = self._register("6700000003", "Manager", "Marketing")
        manager = MarketingManager.objects.get(manager_id=user)
        self.assertTrue(manager.lead_permission.lead)
        self.assertTrue(manager.property_permission.property)

    def test_tenant_lead_gets_property_permission(self):
        from pms_apps.lead.models.lead import Lead

        user = self._register("6700000004", "Employee", "Tenant")
        lead = Lead.objects.get(lead_id=user)
        self.assertIsNotNone(lead.property_permissions)
        self.assertTrue(lead.property_permissions.property)

    def test_every_module_role_combination_registers_successfully(self):
        """Blanket regression: every (module, role) pair the frontend can
        submit at registration must succeed. This would have caught the bug
        where the fix initially assumed every department's Manager/Employee
        model has lead_permission/property_permission fields (true only for
        Marketing and Check-In Check-Out; Maintenance has property_permission
        only; Reception/Finance/Collection/Legal/IT have neither) and crashed
        registration for 5 of 9 departments."""
        from pms_apps.authentication.serializers_auth import UserAuthSerializer

        phone = 6900000000
        for module, roles in UserAuthSerializer.MODULE_TO_ROLE_MAPPINGS.items():
            for role in roles:
                phone += 1
                with self.subTest(module=module, role=role):
                    client = APIClient(HTTP_USER_AGENT="pytest")
                    response = client.post(
                        "/auth/register/",
                        data={"phone_number": str(phone), "role": role, "module": module},
                        format="json",
                    )
                    self.assertEqual(response.status_code, 200, response.data)

        for module in ("Tenant", "Landlord"):
            phone += 1
            with self.subTest(module=module):
                client = APIClient(HTTP_USER_AGENT="pytest")
                response = client.post(
                    "/auth/register/",
                    data={"phone_number": str(phone), "module": module},
                    format="json",
                )
                self.assertEqual(response.status_code, 200, response.data)

    def test_two_managers_get_independent_permission_records(self):
        """Each registration must create its OWN permission row - never
        share one between accounts, since editing one must not silently
        change another's grant."""
        from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager

        user1 = self._register("6700000005", "Manager", "Check-In Check-Out")
        user2 = self._register("6700000006", "Manager", "Check-In Check-Out")
        manager1 = CheckInCheckOutManager.objects.get(manager_id=user1)
        manager2 = CheckInCheckOutManager.objects.get(manager_id=user2)
        self.assertNotEqual(manager1.lead_permission_id, manager2.lead_permission_id)
        self.assertNotEqual(manager1.property_permission_id, manager2.property_permission_id)


class AuthMeEndpointTests(TestCase):
    """GET /auth/me/ must return a caller's own profile regardless of their
    department/role - previously the only way to see this data was a
    department-specific endpoint like /marketing/manager/get/, which 403s
    for every role outside that one department."""

    def tearDown(self):
        from pms_apps.activity_log.middlewares.log_middleware import local
        local.__dict__.clear()

    def _authed_client(self, user):
        token = generate_jwt_token(user)
        user.access_token = token
        user.save()
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client

    def test_marketing_manager_sees_own_profile(self):
        from pms_apps.marketing.models.marketing_manager import MarketingManager
        from pms_apps.common.models.permissions import LeadPermission, PropertyPermission

        user = User.objects.create(
            name="Marketing Manager", phone_number="6800000001", department="Marketing", role="Manager"
        )
        MarketingManager().create(
            manager_id=user.user_id, name="Marketing Manager", dob=None, department="Marketing",
            campaigns_led=0, team_size=0,
            lead_permission_id=LeadPermission().create(lead=True),
            property_permission_id=PropertyPermission().create(property=True),
        )
        response = self._authed_client(user).get("/auth/me/")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["department"], "Marketing")
        self.assertEqual(response.data["role"], "Manager")
        self.assertEqual(response.data["profile"]["manager_id"], user.user_id)

    def test_finance_manager_does_not_403_and_sees_own_profile(self):
        """The core complaint: a non-Marketing role must not 403 when
        fetching its own profile. /auth/me/ lives under /auth/, which is
        exempt from the department-permission gate entirely, so this needs
        no permission grant at all to prove the point."""
        from pms_apps.finance.models.finance_manager import FinanceManager

        user = User.objects.create(
            name="Finance Manager", phone_number="6800000002", department="Finance", role="Manager"
        )
        FinanceManager().create(
            manager_id=user.user_id, name="Finance Manager", dob=None, department="Finance",
            total_budget_managed=0, reports_submitted=0, team_size=0,
        )
        response = self._authed_client(user).get("/auth/me/")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["department"], "Finance")
        self.assertEqual(response.data["profile"]["manager_id"], user.user_id)

    def test_tenant_lead_sees_own_profile(self):
        from pms_apps.lead.models.lead import Lead

        user = User.objects.create(name="Some Tenant", phone_number="6800000003", department="Tenant")
        Lead.objects.create(lead_id=user, first_name="Some", last_name="Tenant", purpose="Tenant")
        response = self._authed_client(user).get("/auth/me/")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["department"], "Tenant")
        self.assertEqual(response.data["profile"]["lead_id"], user.user_id)

    def test_unauthenticated_me_rejected(self):
        client = APIClient(HTTP_USER_AGENT="pytest")
        response = client.get("/auth/me/")
        self.assertEqual(response.status_code, 403)


class JWTAuthenticationMissingDepartmentTests(TestCase):
    """A User with no recognized department (e.g. a row edited via Django
    Admin, which allows department to be left blank) must not crash
    authentication. validate_permissions previously called
    payload.get('department').lower() and permissions_mapping.pop(depeartment)
    unconditionally - a None department raised AttributeError, and a blank
    or unrecognized one raised KeyError. Both must now fail safe instead."""

    def tearDown(self):
        # A real authenticated request sets activity_log's thread-local
        # `local.user_id` (normally reset per-request by LogMiddleware, which
        # only runs for real HTTP requests). These are the first tests in
        # the suite to exercise real JWTAuthentication rather than
        # force_authenticate, so without this cleanup the stale value would
        # leak into later tests that create records directly via the ORM
        # (bypassing the middleware) and log against a since-rolled-back
        # user id.
        from pms_apps.activity_log.middlewares.log_middleware import local
        local.__dict__.clear()

    def _authed_client(self, user):
        token = generate_jwt_token(user)
        user.access_token = token
        user.save()
        client = APIClient(HTTP_USER_AGENT="pytest")
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client

    def test_null_department_does_not_crash_on_unscoped_path(self):
        user = User.objects.create(name="No Department", phone_number="6600000001", department=None)
        response = self._authed_client(user).get("/helper/country/get_all")
        self.assertEqual(response.status_code, 200, response.data)

    def test_blank_department_does_not_crash_on_unscoped_path(self):
        user = User.objects.create(name="Blank Department", phone_number="6600000002", department="")
        response = self._authed_client(user).get("/helper/country/get_all")
        self.assertEqual(response.status_code, 200, response.data)

    def test_null_department_is_denied_not_crashed_on_scoped_path(self):
        """With no department to exempt, every department-guarded path stays
        guarded - a null-department user must be cleanly forbidden (403),
        never crash the request, when hitting a department-scoped endpoint."""
        user = User.objects.create(name="No Department Two", phone_number="6600000003", department=None)
        response = self._authed_client(user).get("/lead/get_all/")
        self.assertEqual(response.status_code, 403, response.data)

    def test_recognized_department_still_exempted_on_own_paths(self):
        """Regression: a User with a normal, recognized department must
        still be able to access their own department's endpoints without
        needing an explicit permission grant for it."""
        user = User.objects.create(name="Finance User", phone_number="6600000004", department="Finance")
        response = self._authed_client(user).get("/finance/manager/get_all/")
        self.assertEqual(response.status_code, 200, response.data)

    def test_recognized_department_still_blocked_from_other_scoped_paths(self):
        """Regression: a User must still be blocked from an unrelated
        department's endpoint when they lack that department's permission."""
        user = User.objects.create(name="Finance User Two", phone_number="6600000005", department="Finance")
        response = self._authed_client(user).get("/lead/get_all/")
        self.assertEqual(response.status_code, 403, response.data)
