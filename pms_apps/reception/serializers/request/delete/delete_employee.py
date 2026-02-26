from rest_framework import serializers
from pms_apps.reception.dataclasses.request.delete.delete_employee import ReceptionEmployeeDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class ReceptionEmployeeDeleteRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()

    def create(self, validated_data) -> ReceptionEmployeeDeleteRequest:
        return ReceptionEmployeeDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='employee_id', description='ID of the reception employee',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]
