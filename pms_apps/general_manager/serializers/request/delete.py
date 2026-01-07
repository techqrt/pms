from rest_framework import serializers
from pms_apps.general_manager.dataclasses.request.delete import GeneralManagerDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class GeneralManagerDeleteRequestSerializer(serializers.Serializer):
    general_manager_id = serializers.IntegerField()

    def create(self, validated_data) -> GeneralManagerDeleteRequest:
        return GeneralManagerDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='general_manager_id', description='ID of the general manager',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]