from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_inspection_item import CheckInInspectionItem
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_inspection_item import (
    CheckInInspectionItemUpdateRequest,
    CheckInInspectionItemDeleteRequest,
)


class CheckInInspectionItemUpdateSerializer(serializers.Serializer):
    check_in_inspection_item_id = serializers.IntegerField()
    category = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInInspectionItem.CATEGORY_CHOICES],
        required=False, allow_null=True
    )
    item_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    inspection_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInInspectionItem.INSPECTION_STATUS_CHOICES],
        required=False, allow_null=True
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
    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckInInspectionItemUpdateRequest:
        return CheckInInspectionItemUpdateRequest(**validated_data)


class CheckInInspectionItemDeleteSerializer(serializers.Serializer):
    check_in_inspection_item_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckInInspectionItemDeleteRequest:
        return CheckInInspectionItemDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_in_inspection_item_id', description='ID of the Check-In Inspection Item',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]