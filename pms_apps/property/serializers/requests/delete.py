from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.property.dataclasses.requests.delete import PropertyDeleteRequest


class PropertyDeleteSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()

    def create(self, validated_data) -> PropertyDeleteRequest:
        return PropertyDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='property_id', description='ID of the property',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
