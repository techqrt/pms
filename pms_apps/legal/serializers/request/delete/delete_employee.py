from rest_framework import serializers
from pms_apps.legal.dataclasses.request.delete.delete_employee import LegalEmployeeDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class LegalEmployeeDeleteRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()

    def create(self, validated_data) -> LegalEmployeeDeleteRequest:
        return LegalEmployeeDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='employee_id', description='ID of the legal employee',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]
