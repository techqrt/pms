from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.authentication.utils import generate_jwt_token


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
