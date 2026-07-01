from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.checkin_checkout.dataclasses.requests.delete_check_out import CheckOutDeleteRequest


class CheckOutDeleteSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckOutDeleteRequest:
        return CheckOutDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='check_out_id', description='ID of the Check-Out',
                             required=True, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
        ]
