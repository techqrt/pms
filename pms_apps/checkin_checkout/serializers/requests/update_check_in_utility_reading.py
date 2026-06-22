from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_utility_reading import CheckInUtilityReading
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_utility_reading import (
    CheckInUtilityReadingUpdateRequest,
    CheckInUtilityReadingDeleteRequest,
)


class CheckInUtilityReadingUpdateSerializer(serializers.Serializer):
    check_in_utility_reading_id = serializers.IntegerField()
    utility_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInUtilityReading.UTILITY_TYPE_CHOICES],
        required=False, allow_null=True
    )
    meter_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    reading_value = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    consumption = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    rate_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    charges = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInUtilityReading.STATUS_CHOICES],
        required=False, allow_null=True
    )
    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckInUtilityReadingUpdateRequest:
        return CheckInUtilityReadingUpdateRequest(**validated_data)


class CheckInUtilityReadingDeleteSerializer(serializers.Serializer):
    check_in_utility_reading_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckInUtilityReadingDeleteRequest:
        return CheckInUtilityReadingDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_in_utility_reading_id', description='ID of the Check-In Utility Reading',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
