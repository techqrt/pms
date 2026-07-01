from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_key import CheckOutKey
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_key import CheckOutKeyCreateRequest


class CheckOutKeyCreateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    key_number = serializers.CharField()
    key_type = serializers.CharField()
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutKey.STATUS_CHOICES],
        required=False, default="Pending"
    )
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckOutKeyCreateRequest:
        return CheckOutKeyCreateRequest(**validated_data)
