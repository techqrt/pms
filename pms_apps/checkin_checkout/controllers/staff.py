from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.checkin_checkout.views.staff import CheckInCheckOutStaffView
from pms_apps.checkin_checkout.serializers.requests.update_manager import CheckInCheckOutManagerUpdateRequestSerializer
from pms_apps.checkin_checkout.serializers.requests.update_employee import CheckInCheckOutEmployeeUpdateRequestSerializer


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

    @extend_schema(
        description="Update a Check-In Check-Out Manager (including permissions)",
        request=CheckInCheckOutManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(description=CheckInCheckOutStaffView().data_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CheckInCheckOutManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return CheckInCheckOutStaffView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Update a Check-In Check-Out Employee (including permissions)",
        request=CheckInCheckOutEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(description=CheckInCheckOutStaffView().data_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CheckInCheckOutEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return CheckInCheckOutStaffView().update_employee_extract(params=request.params)
