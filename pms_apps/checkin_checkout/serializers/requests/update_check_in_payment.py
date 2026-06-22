from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_payment import CheckInPayment
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_payment import (
    CheckInPaymentUpdateRequest,
    CheckInPaymentDeleteRequest,
)


class CheckInPaymentUpdateSerializer(serializers.Serializer):
    check_in_payment_id = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInPayment.STATUS_CHOICES],
        required=False, allow_null=True
    )
    payment_date = serializers.DateField(required=False, allow_null=True)
    receipt_ref_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckInPaymentUpdateRequest:
        return CheckInPaymentUpdateRequest(**validated_data)


class CheckInPaymentDeleteSerializer(serializers.Serializer):
    check_in_payment_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckInPaymentDeleteRequest:
        return CheckInPaymentDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_in_payment_id', description='ID of the Check-In Payment',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
