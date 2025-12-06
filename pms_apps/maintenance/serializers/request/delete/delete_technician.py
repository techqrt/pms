from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.delete.delete_technician import MaintenanceTechnicianDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class MaintenanceTechnicianDeleteRequestSerializer(serializers.Serializer):
    technician_id = serializers.IntegerField()

    def create(self, validated_data) -> MaintenanceTechnicianDeleteRequest:
        return MaintenanceTechnicianDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='technician_id', description='ID of the maintenance technician',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]