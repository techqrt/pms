from rest_framework import serializers
from pms_apps.common.serializers.request.get import GetSerializer
from pms_apps.legal.dataclasses.request.get.get_employee import LegalEmployeeGetRequest
from pms_apps.common.swagger import SwaggerPage
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class LegalEmployeeGetRequestSerializer(GetSerializer):
    employee_id = serializers.IntegerField()

    def create(self, validated_data) -> LegalEmployeeGetRequest:
        return LegalEmployeeGetRequest(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()) -> list:
        default_parameters.append(OpenApiParameter(
            name='employee_id', description='ID of the legal employee',
            required=True, type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY
        ))
        return default_parameters
