from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_inspection_item import CheckInInspectionItem
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_inspection_item import (
    CheckInInspectionItemCreateRequest,
)


class CheckInInspectionItemCreateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    category = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInInspectionItem.CATEGORY_CHOICES]
    )
    item_name = serializers.CharField()
    inspection_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInInspectionItem.INSPECTION_STATUS_CHOICES]
    )
    severity = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInInspectionItem.SEVERITY_CHOICES],
        required=False, allow_null=True
    )
    repair_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInInspectionItem.REPAIR_STATUS_CHOICES],
        required=False, allow_null=True
    )
    item_approval_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInInspectionItem.ITEM_APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True)
    target_date = serializers.DateField(required=False, allow_null=True)
    photo = serializers.CharField(required=False, allow_null=True)
    remarks = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckInInspectionItemCreateRequest:
        return CheckInInspectionItemCreateRequest(**validated_data)