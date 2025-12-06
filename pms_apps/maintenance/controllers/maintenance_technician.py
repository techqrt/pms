from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.maintenance.serializers.request.create.create_technician import MaintenanceTechnicianCreateRequestSerializer
from pms_apps.maintenance.serializers.request.update.update_technician import MaintenanceTechnicianUpdateRequestSerializer
from pms_apps.maintenance.serializers.request.delete.delete_technician import MaintenanceTechnicianDeleteRequestSerializer
from pms_apps.maintenance.serializers.request.get.get_technician import MaintenanceTechnicianGetRequestSerializer
from pms_apps.maintenance.serializers.response.get.get_technician import MaintenanceTechnicianResponseGetSerializer
from pms_apps.maintenance.serializers.response.get_all.get_all_technician import MaintenanceTechnicianResponseGetAllSerializer

from pms_apps.maintenance.views.maintenance_technician import MaintenanceTechnicianView


class MaintenanceTechnicianViewController:
    @extend_schema(
        description="Add a Maintenance Technician",
        request=MaintenanceTechnicianCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=MaintenanceTechnicianView().technician_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceTechnicianCreateRequestSerializer).validate
    def create_technician(request: Request) -> Response:
        return MaintenanceTechnicianView().create_technician_extract(params=request.params)

    @extend_schema(
        description="Update a Maintenance Technician",
        request=MaintenanceTechnicianUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=MaintenanceTechnicianView().technician_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceTechnicianUpdateRequestSerializer).validate
    def update_technician(request: Request) -> Response:
        return MaintenanceTechnicianView().update_technician_extract(params=request.params)

    @extend_schema(
        description="Delete a Maintenance Technician",
        parameters=MaintenanceTechnicianDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=MaintenanceTechnicianView().technician_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceTechnicianDeleteRequestSerializer).validate
    def delete_technician(request: Request) -> Response:
        return MaintenanceTechnicianView().delete_technician_extract(params=request.params)

    @extend_schema(
        description="Get a Maintenance Technician",
        parameters=MaintenanceTechnicianGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=MaintenanceTechnicianResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MaintenanceTechnicianGetRequestSerializer).validate
    def get_technician(request: Request) -> Response:
        return MaintenanceTechnicianView().get_technician_extract(params=request.params)

    @extend_schema(
        description="Get all Maintenance Technicians",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=MaintenanceTechnicianResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_technician(request: Request) -> Response:
        return MaintenanceTechnicianView().get_all_technician_extract(params=request.params)
