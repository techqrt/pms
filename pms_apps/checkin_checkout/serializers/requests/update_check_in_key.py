from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_key import CheckInKey
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_key import (
    CheckInKeyUpdateRequest,
    CheckInKeyDeleteRequest,
)


class CheckInKeyUpdateSerializer(serializers.Serializer):
    check_in_key_id = serializers.IntegerField()
    key_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    key_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInKey.STATUS_CHOICES],
        required=False, allow_null=True
    )
    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckInKeyUpdateRequest:
        return CheckInKeyUpdateRequest(**validated_data)


class CheckInKeyDeleteSerializer(serializers.Serializer):
    check_in_key_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckInKeyDeleteRequest:
        return CheckInKeyDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_in_key_id', description='ID of the Check-In Key',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
