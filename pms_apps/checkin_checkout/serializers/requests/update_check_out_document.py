from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_document import (
    CheckOutDocumentUpdateRequest,
    CheckOutDocumentDeleteRequest,
)


class CheckOutDocumentUpdateSerializer(serializers.Serializer):
    check_out_document_id = serializers.IntegerField()
    document_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    linked_to_label = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckOutDocumentUpdateRequest:
        return CheckOutDocumentUpdateRequest(**validated_data)


class CheckOutDocumentDeleteSerializer(serializers.Serializer):
    check_out_document_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckOutDocumentDeleteRequest:
        return CheckOutDocumentDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_out_document_id',
                             description='ID of the Check-Out Document',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
