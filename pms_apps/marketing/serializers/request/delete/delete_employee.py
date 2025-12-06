from rest_framework import serializers
from pms_apps.marketing.dataclasses.request.delete.delete_employee import MarketingEmployeeDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class MarketingEmployeeDeleteRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()

    def create(self, validated_data) -> MarketingEmployeeDeleteRequest:
        return MarketingEmployeeDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='employee_id', description='ID of the marketing employee',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]
