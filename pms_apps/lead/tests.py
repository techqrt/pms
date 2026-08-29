from django.test import TestCase

from pms_apps.lead.serilizers.request.create import LeadCreateRequestSerilizer


class LeadCreateRequestSerilizerTests(TestCase):
    """Validation tests for Create Lead: only first_name, last_name,
    phone_number (contact number), purpose (lead type) and lead_category
    are mandatory; every other field must be optional."""

    def minimal_payload(self):
        return {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "purpose": "Tenant",
            "lead_category": "Bachelor",
        }

    def test_valid_minimal_lead(self):
        serializer = LeadCreateRequestSerilizer(data=self.minimal_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_optional_fields_omitted_succeeds(self):
        payload = self.minimal_payload()
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        for field in (
            "lead_origin", "nationality", "passport_or_id",
            "civil_id", "po_box", "feedback", "lead_assign_to",
            "address", "country", "city",
        ):
            self.assertNotIn(field, serializer.errors)

    def test_optional_fields_as_blank_strings_succeeds(self):
        payload = self.minimal_payload()
        payload.update({
            "passport_or_id": "",
            "civil_id": "",
            "po_box": "",
            "feedback": "",
            "lead_origin": "",
            "address": "",
        })
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_first_name_fails(self):
        payload = self.minimal_payload()
        del payload["first_name"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_missing_last_name_fails(self):
        payload = self.minimal_payload()
        del payload["last_name"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_missing_contact_number_fails(self):
        payload = self.minimal_payload()
        del payload["phone_number"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)

    def test_missing_lead_type_fails(self):
        payload = self.minimal_payload()
        del payload["purpose"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("purpose", serializer.errors)

    def test_missing_lead_category_fails(self):
        payload = self.minimal_payload()
        del payload["lead_category"]
        serializer = LeadCreateRequestSerilizer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("lead_category", serializer.errors)

    def test_create_builds_request_with_none_for_omitted_optional_fields(self):
        serializer = LeadCreateRequestSerilizer(data=self.minimal_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)
        request = serializer.save()

        self.assertEqual(request.first_name, "John")
        self.assertEqual(request.last_name, "Doe")
        self.assertEqual(request.phone_number, "1234567890")
        self.assertEqual(request.purpose, "Tenant")
        self.assertEqual(request.lead_category, "Bachelor")
        self.assertIsNone(request.lead_origin)
        self.assertIsNone(request.nationality_id)
        self.assertIsNone(request.passport_or_id)
        self.assertIsNone(request.civil_id)
        self.assertIsNone(request.po_box)
        self.assertIsNone(request.feedback)
        self.assertIsNone(request.lead_assign_to)
        self.assertIsNone(request.address)
        self.assertIsNone(request.country_id)
        self.assertIsNone(request.city_id)
