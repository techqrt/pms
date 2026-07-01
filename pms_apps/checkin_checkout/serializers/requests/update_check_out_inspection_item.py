from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_inspection_item import CheckOutInspectionItem
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_inspection_item import (
    CheckOutInspectionItemUpdateRequest,
    CheckOutInspectionItemDeleteRequest,
)


class CheckOutInspectionItemUpdateSerializer(serializers.Serializer):
    check_out_inspection_item_id = serializers.IntegerField()
    category = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutInspectionItem.CATEGORY_CHOICES],
        required=False, allow_null=True
    )
    item_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    inspection_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutInspectionItem.INSPECTION_STATUS_CHOICES],
        required=False, allow_null=True
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
    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckOutInspectionItemUpdateRequest:
        return CheckOutInspectionItemUpdateRequest(**validated_data)


class CheckOutInspectionItemDeleteSerializer(serializers.Serializer):
    check_out_inspection_item_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckOutInspectionItemDeleteRequest:
        return CheckOutInspectionItemDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_out_inspection_item_id',
                             description='ID of the Check-Out Inspection Item',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
