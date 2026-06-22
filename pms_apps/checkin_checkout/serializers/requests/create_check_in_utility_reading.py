from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_utility_reading import CheckInUtilityReading
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_utility_reading import (
    CheckInUtilityReadingCreateRequest,
)


class CheckInUtilityReadingCreateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    utility_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInUtilityReading.UTILITY_TYPE_CHOICES]
    )
    meter_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    reading_value = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    consumption = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    rate_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    charges = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInUtilityReading.STATUS_CHOICES],
        default="Normal"
    )
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckInUtilityReadingCreateRequest:
        return CheckInUtilityReadingCreateRequest(**validated_data)
