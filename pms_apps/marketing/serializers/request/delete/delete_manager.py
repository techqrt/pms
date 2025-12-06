from rest_framework import serializers
from pms_apps.marketing.dataclasses.request.delete.delete_manager import MarketingManagerDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


class MarketingManagerDeleteRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def create(self, validated_data) -> MarketingManagerDeleteRequest:
        return MarketingManagerDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='manager_id', description='ID of the marketing manager',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]
