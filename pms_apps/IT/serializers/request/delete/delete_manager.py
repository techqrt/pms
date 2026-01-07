from rest_framework import serializers
from pms_apps.IT.dataclasses.request.delete.delete_manager import ITManagerDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class ITManagerDeleteRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def create(self, validated_data) -> ITManagerDeleteRequest:
        return ITManagerDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='manager_id', description='ID of the IT manager',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]