from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.property.dataclasses.requests.building_delete import BuildingDeleteRequest


class BuildingDeleteSerializer(serializers.Serializer):
    building_id = serializers.IntegerField()

    def create(self, validated_data) -> BuildingDeleteRequest:
        return BuildingDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='building_id', description='ID of the building',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
