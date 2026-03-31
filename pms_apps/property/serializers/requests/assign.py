from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.property.dataclasses.requests.assign import PropertyAssignRequest


class PropertyAssignSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    tenant_id = serializers.IntegerField()

    def create(self, validated_data) -> PropertyAssignRequest:
        return PropertyAssignRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='property_id', description='ID of the property',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='tenant_id', description='ID of the tenant (Lead ID)',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
