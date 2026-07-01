from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_payment import CheckOutPayment
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_payment import (
    CheckOutPaymentUpdateRequest,
    CheckOutPaymentDeleteRequest,
)


class CheckOutPaymentUpdateSerializer(serializers.Serializer):
    check_out_payment_id = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    tax = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutPayment.STATUS_CHOICES],
        required=False, allow_null=True
    )
    payment_date = serializers.DateField(required=False, allow_null=True)
    receipt_ref_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckOutPaymentUpdateRequest:
        return CheckOutPaymentUpdateRequest(**validated_data)


class CheckOutPaymentDeleteSerializer(serializers.Serializer):
    check_out_payment_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckOutPaymentDeleteRequest:
        return CheckOutPaymentDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_out_payment_id',
                             description='ID of the Check-Out Payment',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
