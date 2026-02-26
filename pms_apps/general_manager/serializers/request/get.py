from rest_framework import serializers
from pms_apps.common.serializers.request.get import GetSerializer
from pms_apps.general_manager.dataclasses.request.get import GeneralManagerGetRequest
from pms_apps.common.swagger import SwaggerPage
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class GeneralManagerGetRequestSerializer(GetSerializer):
    general_manager_id = serializers.IntegerField()

    def create(self, validated_data) -> GeneralManagerGetRequest:
        return GeneralManagerGetRequest(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()) -> list:
        default_parameters.append(OpenApiParameter(
            name='general_manager_id', description='ID of the general manager',
            required=True, type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY
        ))
        return default_parameters
