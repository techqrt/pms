from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.reception.serializers.request.create.create_manager import ReceptionManagerCreateRequestSerializer
from pms_apps.reception.serializers.request.update.update_manager import ReceptionManagerUpdateRequestSerializer
from pms_apps.reception.serializers.request.delete.delete_manager import ReceptionManagerDeleteRequestSerializer
from pms_apps.reception.serializers.request.get.get_manager import ReceptionManagerGetRequestSerializer
from pms_apps.reception.serializers.response.get.get_manager import ReceptionManagerResponseGetSerializer
from pms_apps.reception.serializers.response.get_all.get_all_manager import ReceptionManagerResponseGetAllSerializer
from pms_apps.reception.views.reception_manager import ReceptionManagerView

class ReceptionManagerViewController:
    @extend_schema(
        description="Add a Reception Manager",
        request=ReceptionManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=ReceptionManagerView().manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionManagerCreateRequestSerializer).validate
    def create_manager(request: Request) -> Response:
        return ReceptionManagerView().create_manager_extract(params=request.params)

    @extend_schema(
        description="Update a Reception Manager",
        request=ReceptionManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=ReceptionManagerView().manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return ReceptionManagerView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a Reception Manager",
        parameters=ReceptionManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=ReceptionManagerView().manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionManagerDeleteRequestSerializer).validate
    def delete_manager(request: Request) -> Response:
        return ReceptionManagerView().delete_manager_extract(params=request.params)

    @extend_schema(
        description="Get a Reception Manager",
        parameters=ReceptionManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=ReceptionManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionManagerGetRequestSerializer).validate
    def get_manager(request: Request) -> Response:
        return ReceptionManagerView().get_manager_extract(params=request.params)

    @extend_schema(
        description="Get all Reception Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=ReceptionManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return ReceptionManagerView().get_all_manager_extract(params=request.params)
