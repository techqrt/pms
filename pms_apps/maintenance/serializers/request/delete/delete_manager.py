from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.delete.delete_manager import MaintenanceManagerDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class MaintenanceManagerDeleteRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def create(self, validated_data) -> MaintenanceManagerDeleteRequest:
        return MaintenanceManagerDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='manager_id', description='ID of the maintenance manager',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]