from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.checkin_checkout.views.staff import CheckInCheckOutStaffView


class CheckInCheckOutStaffViewController:
    @extend_schema(
        description="Get all Check-In Check-Out Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckInCheckOutStaffView().data_get)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return CheckInCheckOutStaffView().get_all_manager_extract(params=request.params)

    @extend_schema(
        description="Get all Check-In Check-Out Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckInCheckOutStaffView().data_get)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return CheckInCheckOutStaffView().get_all_employee_extract(params=request.params)
