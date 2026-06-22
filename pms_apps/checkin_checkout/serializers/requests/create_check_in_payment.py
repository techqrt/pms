from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_payment import CheckInPayment
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_payment import (
    CheckInPaymentCreateRequest,
)


class CheckInPaymentCreateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    description = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInPayment.STATUS_CHOICES],
        default="Pending"
    )
    payment_date = serializers.DateField(required=False, allow_null=True)
    receipt_ref_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckInPaymentCreateRequest:
        return CheckInPaymentCreateRequest(**validated_data)
