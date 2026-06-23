from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from pms_apps.common.serializers.request.get import GetSerializer
from pms_apps.common.swagger import SwaggerPage
from pms_apps.checkin_checkout.dataclasses.requests.get_check_out import CheckOutGetRequest


class CheckOutGetSerializer(GetSerializer):
    check_out_id = serializers.IntegerField()

    def create(self, validated_data) -> CheckOutGetRequest:
        return CheckOutGetRequest(check_out_id=validated_data['check_out_id'])

    @staticmethod
    def get_parameters(default_parameters: list = None):
        default_parameters = default_parameters or SwaggerPage.get_parameters()
        default_parameters.append(OpenApiParameter(
            name='check_out_id', description='ID of the Check-Out',
            required=True, type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY
        ))
        return default_parameters
