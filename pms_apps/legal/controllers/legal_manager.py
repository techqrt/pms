from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.legal.serializers.request.create.create_manager import LegalManagerCreateRequestSerializer
from pms_apps.legal.serializers.request.update.update_manager import LegalManagerUpdateRequestSerializer
from pms_apps.legal.serializers.request.delete.delete_manager import LegalManagerDeleteRequestSerializer
from pms_apps.legal.serializers.request.get.get_manager import LegalManagerGetRequestSerializer
from pms_apps.legal.serializers.response.get.get_manager import LegalManagerResponseGetSerializer
from pms_apps.legal.serializers.response.get_all.get_all_manager import LegalManagerResponseGetAllSerializer
from pms_apps.legal.views.legal_manager import LegalManagerView

class LegalManagerViewController:
    @extend_schema(
        description="Add a Legal Manager",
        request=LegalManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=LegalManagerView().manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalManagerCreateRequestSerializer).validate
    def create_manager(request: Request) -> Response:
        return LegalManagerView().create_manager_extract(params=request.params)

    @extend_schema(
        description="Update a Legal Manager",
        request=LegalManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=LegalManagerView().manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return LegalManagerView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a Legal Manager",
        parameters=LegalManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=LegalManagerView().manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalManagerDeleteRequestSerializer).validate
    def delete_manager(request: Request) -> Response:
        return LegalManagerView().delete_manager_extract(params=request.params)

    @extend_schema(
        description="Get a Legal Manager",
        parameters=LegalManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=LegalManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalManagerGetRequestSerializer).validate
    def get_manager(request: Request) -> Response:
        return LegalManagerView().get_manager_extract(params=request.params)

    @extend_schema(
        description="Get all Legal Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=LegalManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return LegalManagerView().get_all_manager_extract(params=request.params)
