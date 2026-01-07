from rest_framework import serializers
from pms_apps.owner.dataclasses.request.delete import OwnerDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class OwnerDeleteRequestSerializer(serializers.Serializer):
    owner_id = serializers.IntegerField()

    def create(self, validated_data) -> OwnerDeleteRequest:
        return OwnerDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='owner_id', description='ID of the owner',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]