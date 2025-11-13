from rest_framework import serializers
from pms_apps.lead.dataclasses.request.get import LeadGetRequest
from pms_apps.common.swagger import SwaggerPage
from drf_spectacular.types import OpenApiTypes
from pms_apps.common.serializers.request.get import GetSerializer
from drf_spectacular.utils import OpenApiParameter


class LeadGetRequestSerilizer(GetSerializer):
    lead_id = serializers.IntegerField()

    def create(self, validated_data) -> LeadGetRequest:
        return LeadGetRequest(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()) -> list:
        default_parameters.append(OpenApiParameter(name='lead_id', description='ID of the lead',
                                                   required=True, type=OpenApiTypes.INT,
                                                   location=OpenApiParameter.QUERY))
        return default_parameters