from rest_framework import serializers
from pms_apps.reception.dataclasses.request.delete.delete_manager import ReceptionManagerDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class ReceptionManagerDeleteRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def create(self, validated_data) -> ReceptionManagerDeleteRequest:
        return ReceptionManagerDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='manager_id', description='ID of the reception manager',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]