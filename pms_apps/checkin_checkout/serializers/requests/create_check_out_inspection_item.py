from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_inspection_item import CheckOutInspectionItem
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_inspection_item import (
    CheckOutInspectionItemCreateRequest,
)


class CheckOutInspectionItemCreateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    category = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutInspectionItem.CATEGORY_CHOICES]
    )
    item_name = serializers.CharField()
    inspection_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutInspectionItem.INSPECTION_STATUS_CHOICES]
    )
    severity = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutInspectionItem.SEVERITY_CHOICES],
        required=False, allow_null=True
    )
    repair_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutInspectionItem.REPAIR_STATUS_CHOICES],
        required=False, allow_null=True
    )
    item_approval_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutInspectionItem.ITEM_APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True)
    target_date = serializers.DateField(required=False, allow_null=True)
    cost = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    photo = serializers.CharField(required=False, allow_null=True)
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckOutInspectionItemCreateRequest:
        return CheckOutInspectionItemCreateRequest(**validated_data)
