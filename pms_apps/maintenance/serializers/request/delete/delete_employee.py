from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.delete.delete_employee import MaintenanceEmpleoyeeDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class MaintenanceEmployeeDeleteRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()

    def create(self, validated_data) -> MaintenanceEmpleoyeeDeleteRequest:
        return MaintenanceEmpleoyeeDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='employee_id', description='ID of the maintenance employee',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]
