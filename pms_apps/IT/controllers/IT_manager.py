from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.IT.serializers.request.create.create_manager import ITManagerCreateRequestSerializer
from pms_apps.IT.serializers.request.update.update_manager import ITManagerUpdateRequestSerializer
from pms_apps.IT.serializers.request.delete.delete_manager import ITManagerDeleteRequestSerializer
from pms_apps.IT.serializers.request.get.get_manager import ITManagerGetRequestSerializer
from pms_apps.IT.serializers.response.get.get_manager import ITManagerResponseGetSerializer
from pms_apps.IT.serializers.response.get_all.get_all_manager import ITManagerResponseGetAllSerializer
from pms_apps.IT.views.IT_manager import ITManagerView

class ITManagerViewController:
    @extend_schema(
        description="Add a IT Manager",
        request=ITManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=ITManagerView().manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITManagerCreateRequestSerializer).validate
    def create_manager(request: Request) -> Response:
        return ITManagerView().create_manager_extract(params=request.params)

    @extend_schema(
        description="Update a IT Manager",
        request=ITManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=ITManagerView().manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return ITManagerView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a IT Manager",
        parameters=ITManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=ITManagerView().manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITManagerDeleteRequestSerializer).validate
    def delete_manager(request: Request) -> Response:
        return ITManagerView().delete_manager_extract(params=request.params)

    @extend_schema(
        description="Get a IT Manager",
        parameters=ITManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=ITManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITManagerGetRequestSerializer).validate
    def get_manager(request: Request) -> Response:
        return ITManagerView().get_manager_extract(params=request.params)

    @extend_schema(
        description="Get all IT Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=ITManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return ITManagerView().get_all_manager_extract(params=request.params)
