from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.maintenance.serializers.request.create.create_manager import MaintenanceManagerCreateRequestSerializer
from pms_apps.maintenance.serializers.request.update.update_manager import MaintenanceManagerUpdateRequestSerializer
from pms_apps.maintenance.serializers.request.delete.delete_manager import MaintenanceManagerDeleteRequestSerializer
from pms_apps.maintenance.serializers.request.get.get_manager import MaintenanceManagerGetRequestSerializer
from pms_apps.maintenance.serializers.response.get.get_manager import MaintenanceManagerResponseGetSerializer
from pms_apps.maintenance.serializers.response.get_all.get_all_manager import MaintenanceManagerResponseGetAllSerializer
from pms_apps.maintenance.views.maintenance_manager import MaintenanceManagerView

class MaintenanceManagerViewController:
    @extend_schema(
        description="Add a Maintenance Manager",
        request=MaintenanceManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=MaintenanceManagerView().manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceManagerCreateRequestSerializer).validate
    def create_manager(request: Request) -> Response:
        return MaintenanceManagerView().create_manager_extract(params=request.params)

    @extend_schema(
        description="Update a Maintenance Manager",
        request=MaintenanceManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=MaintenanceManagerView().manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return MaintenanceManagerView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a Maintenance Manager",
        parameters=MaintenanceManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=MaintenanceManagerView().manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceManagerDeleteRequestSerializer).validate
    def delete_manager(request: Request) -> Response:
        return MaintenanceManagerView().delete_manager_extract(params=request.params)

    @extend_schema(
        description="Get a Maintenance Manager",
        parameters=MaintenanceManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=MaintenanceManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceManagerGetRequestSerializer).validate
    def get_manager(request: Request) -> Response:
        return MaintenanceManagerView().get_manager_extract(params=request.params)

    @extend_schema(
        description="Get all Maintenance Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=MaintenanceManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return MaintenanceManagerView().get_all_manager_extract(params=request.params)
