from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.common.serializers.request.get import GetSerializer
from pms_apps.common.swagger import SwaggerPage
from pms_apps.property.dataclasses.requests.get import PropertyGetRequest


class PropertyGetSerializer(GetSerializer):
    property_id = serializers.IntegerField()

    def create(self, validated_data) -> PropertyGetRequest:
        return PropertyGetRequest(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()) -> list:
        default_parameters.append(OpenApiParameter(name='property_id', description='ID of the property',
                                                   required=True, type=OpenApiTypes.INT,
                                                   location=OpenApiParameter.QUERY))
        return default_parameters
