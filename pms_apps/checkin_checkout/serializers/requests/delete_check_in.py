from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.dataclasses.requests.delete_check_in import CheckInDeleteRequest


class CheckInDeleteSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckInDeleteRequest:
        return CheckInDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_in_id', description='ID of the Check-In',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
