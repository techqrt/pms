from rest_framework import serializers
from pms_apps.common.serializers.request.get import GetSerializer
from pms_apps.legal.dataclasses.request.get.get_manager import LegalManagerGetRequest
from pms_apps.common.swagger import SwaggerPage
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class LegalManagerGetRequestSerializer(GetSerializer):
    manager_id = serializers.IntegerField()

    def create(self, validated_data) -> LegalManagerGetRequest:
        return LegalManagerGetRequest(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()) -> list:
        default_parameters.append(OpenApiParameter(
            name='manager_id', description='ID of the legal manager',
            required=True, type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY
        ))
        return default_parameters
