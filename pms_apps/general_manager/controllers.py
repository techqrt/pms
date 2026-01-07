from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.general_manager.serializers.request.create import GeneralManagerCreateRequestSerializer
from pms_apps.general_manager.serializers.request.update import GeneralManagerUpdateRequestSerializer
from pms_apps.general_manager.serializers.request.delete import GeneralManagerDeleteRequestSerializer
from pms_apps.general_manager.serializers.request.get import GeneralManagerGetRequestSerializer
from pms_apps.general_manager.serializers.response.get import GeneralManagerResponseGetSerializer
from pms_apps.general_manager.serializers.response.get_all import GeneralManagerResponseGetAllSerializer
from pms_apps.general_manager.views import GeneralManagerView

class GeneralManagerViewController:
    @extend_schema(
        description="Add a General Manager",
        request=GeneralManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=GeneralManagerView().general_manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GeneralManagerCreateRequestSerializer).validate
    def create_general_manager(request: Request) -> Response:
        return GeneralManagerView().create_general_manager_extract(params=request.params)

    @extend_schema(
        description="Update a General Manager",
        request=GeneralManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=GeneralManagerView().general_manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GeneralManagerUpdateRequestSerializer).validate
    def update_general_manager(request: Request) -> Response:
        return GeneralManagerView().update_general_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a General Manager",
        parameters=GeneralManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=GeneralManagerView().general_manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GeneralManagerDeleteRequestSerializer).validate
    def delete_general_manager(request: Request) -> Response:
        return GeneralManagerView().delete_general_manager_extract(params=request.params)

    @extend_schema(
        description="Get a General Manager",
        parameters=GeneralManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=GeneralManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GeneralManagerGetRequestSerializer).validate
    def get_general_manager(request: Request) -> Response:
        return GeneralManagerView().get_general_manager_extract(params=request.params)

    @extend_schema(
        description="Get all General Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=GeneralManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_general_manager(request: Request) -> Response:
        return GeneralManagerView().get_all_general_manager_extract(params=request.params)
