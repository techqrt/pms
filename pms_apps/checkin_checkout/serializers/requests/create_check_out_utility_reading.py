from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_utility_reading import CheckOutUtilityReading
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_utility_reading import (
    CheckOutUtilityReadingCreateRequest,
)


class CheckOutUtilityReadingCreateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    utility_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutUtilityReading.UTILITY_TYPE_CHOICES]
    )
    meter_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    reading_value = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    consumption = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    rate_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    charges = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutUtilityReading.STATUS_CHOICES],
        required=False, default="Normal"
    )
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckOutUtilityReadingCreateRequest:
        return CheckOutUtilityReadingCreateRequest(**validated_data)
