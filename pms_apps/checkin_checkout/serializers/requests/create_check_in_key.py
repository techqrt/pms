from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_key import CheckInKey
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_key import (
    CheckInKeyCreateRequest,
)


class CheckInKeyCreateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    key_number = serializers.CharField()
    key_type = serializers.CharField()
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInKey.STATUS_CHOICES],
        default="Pending"
    )
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckInKeyCreateRequest:
        return CheckInKeyCreateRequest(**validated_data)
