from django.test import TestCase
from rest_framework.test import APIClient

from pms_apps.authentication.models import User
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.common.models.permissions import LeadPermission, PropertyPermission


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
