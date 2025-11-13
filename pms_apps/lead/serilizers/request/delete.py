from rest_framework import serializers
from pms_apps.lead.dataclasses.request.delete import LeadDeleteRequest
from pms_apps.common.swagger import SwaggerPage
from drf_spectacular.types import OpenApiTypes
from pms_apps.common.serializers.request.get import GetSerializer
from drf_spectacular.utils import OpenApiParameter

class LeadDeleteRequestSerilizer(serializers.Serializer):
    lead_id = serializers.IntegerField()

    def create(self, validated_data) -> LeadDeleteRequest:
        return LeadDeleteRequest(**validated_data)
    
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='lead_id', description='ID of the lead',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]