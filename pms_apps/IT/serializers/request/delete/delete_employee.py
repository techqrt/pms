from rest_framework import serializers
from pms_apps.IT.dataclasses.request.delete.delete_employee import ITEmployeeDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class ITEmployeeDeleteRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()

    def create(self, validated_data) -> ITEmployeeDeleteRequest:
        return ITEmployeeDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='employee_id', description='ID of the IT employee',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]
