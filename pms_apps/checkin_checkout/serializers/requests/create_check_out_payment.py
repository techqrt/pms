from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_payment import CheckOutPayment
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_payment import CheckOutPaymentCreateRequest


class CheckOutPaymentCreateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    description = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    tax = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutPayment.STATUS_CHOICES],
        required=False, default="Pending"
    )
    payment_method = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutPayment.PAYMENT_METHOD_CHOICES],
        required=False, allow_null=True
    )
    payment_date = serializers.DateField(required=False, allow_null=True)
    receipt_ref_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckOutPaymentCreateRequest:
        return CheckOutPaymentCreateRequest(**validated_data)
