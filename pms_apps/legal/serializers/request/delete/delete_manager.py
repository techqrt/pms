from rest_framework import serializers
from pms_apps.legal.dataclasses.request.delete.delete_manager import LegalManagerDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class LegalManagerDeleteRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def create(self, validated_data) -> LegalManagerDeleteRequest:
        return LegalManagerDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='manager_id', description='ID of the legal manager',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]