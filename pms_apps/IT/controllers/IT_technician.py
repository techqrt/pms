from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.IT.serializers.request.create.create_technician import ITTechnicianCreateRequestSerializer
from pms_apps.IT.serializers.request.update.update_technician import ITTechnicianUpdateRequestSerializer
from pms_apps.IT.serializers.request.delete.delete_technician import ITTechnicianDeleteRequestSerializer
from pms_apps.IT.serializers.request.get.get_technician import ITTechnicianGetRequestSerializer
from pms_apps.IT.serializers.response.get.get_technician import ITTechnicianResponseGetSerializer
from pms_apps.IT.serializers.response.get_all.get_all_technician import ITTechnicianResponseGetAllSerializer
from pms_apps.IT.views.IT_technician import ITTechnicianView


class ITTechnicianViewController:
    @extend_schema(
        description="Add a IT Technician",
        request=ITTechnicianCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=ITTechnicianView().technician_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITTechnicianCreateRequestSerializer).validate
    def create_technician(request: Request) -> Response:
        return ITTechnicianView().create_technician_extract(params=request.params)

    @extend_schema(
        description="Update a IT Technician",
        request=ITTechnicianUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=ITTechnicianView().technician_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITTechnicianUpdateRequestSerializer).validate
    def update_technician(request: Request) -> Response:
        return ITTechnicianView().update_technician_extract(params=request.params)

    @extend_schema(
        description="Delete a IT Technician",
        parameters=ITTechnicianDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=ITTechnicianView().technician_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITTechnicianDeleteRequestSerializer).validate
    def delete_technician(request: Request) -> Response:
        return ITTechnicianView().delete_technician_extract(params=request.params)

    @extend_schema(
        description="Get a IT Technician",
        parameters=ITTechnicianGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=ITTechnicianResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITTechnicianGetRequestSerializer).validate
    def get_technician(request: Request) -> Response:
        return ITTechnicianView().get_technician_extract(params=request.params)

    @extend_schema(
        description="Get all IT Technicians",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=ITTechnicianResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_technician(request: Request) -> Response:
        return ITTechnicianView().get_all_technician_extract(params=request.params)
