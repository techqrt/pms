from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.maintenance.serializers.request.create.create_employee import MaintenanceEmployeeCreateRequestSerializer
from pms_apps.maintenance.serializers.request.update.update_employee import MaintenanceEmployeeUpdateRequestSerializer
from pms_apps.maintenance.serializers.request.delete.delete_employee import MaintenanceEmployeeDeleteRequestSerializer
from pms_apps.maintenance.serializers.request.get.get_employee import MaintenanceEmployeeGetRequestSerializer
from pms_apps.maintenance.serializers.response.get.get_employee import MaintenanceEmployeeResponseGetSerializer
from pms_apps.maintenance.serializers.response.get_all.get_all_employee import MaintenanceEmployeeResponseGetAllSerializer

from pms_apps.maintenance.views.maintenance_employee import MaintenanceEmployeeView


class MaintenanceEmployeeViewController:
    @extend_schema(
        description="Add a Maintenance Employee",
        request=MaintenanceEmployeeCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=MaintenanceEmployeeView().employee_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceEmployeeCreateRequestSerializer).validate
    def create_employee(request: Request) -> Response:
        return MaintenanceEmployeeView().create_employee_extract(params=request.params)

    @extend_schema(
        description="Update a Maintenance Employee",
        request=MaintenanceEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=MaintenanceEmployeeView().employee_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return MaintenanceEmployeeView().update_employee_extract(params=request.params)

    @extend_schema(
        description="Delete a Maintenance Employee",
        parameters=MaintenanceEmployeeDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=MaintenanceEmployeeView().employee_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceEmployeeDeleteRequestSerializer).validate
    def delete_employee(request: Request) -> Response:
        return MaintenanceEmployeeView().delete_employee_extract(params=request.params)

    @extend_schema(
        description="Get a Maintenance Employee",
        parameters=MaintenanceEmployeeGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=MaintenanceEmployeeResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceEmployeeGetRequestSerializer).validate
    def get_employee(request: Request) -> Response:
        return MaintenanceEmployeeView().get_employee_extract(params=request.params)

    @extend_schema(
        description="Get all Maintenance Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=MaintenanceEmployeeResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return MaintenanceEmployeeView().get_all_employee_extract(params=request.params)
