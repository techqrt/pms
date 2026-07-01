from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_key import CheckOutKey
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_key import (
    CheckOutKeyUpdateRequest,
    CheckOutKeyDeleteRequest,
)


class CheckOutKeyUpdateSerializer(serializers.Serializer):
    check_out_key_id = serializers.IntegerField()
    key_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    key_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutKey.STATUS_CHOICES],
        required=False, allow_null=True
    )
    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckOutKeyUpdateRequest:
        return CheckOutKeyUpdateRequest(**validated_data)


class CheckOutKeyDeleteSerializer(serializers.Serializer):
    check_out_key_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckOutKeyDeleteRequest:
        return CheckOutKeyDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_out_key_id',
                             description='ID of the Check-Out Key',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
