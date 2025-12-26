from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.marketing.serializers.request.create.create_manager import MarketingManagerCreateRequestSerializer
from pms_apps.marketing.serializers.request.update.update_manager import MarketingManagerUpdateRequestSerializer
from pms_apps.marketing.serializers.request.delete.delete_manager import MarketingManagerDeleteRequestSerializer
from pms_apps.marketing.serializers.request.get.get_manager import MarketingManagerGetRequestSerializer
from pms_apps.marketing.serializers.response.get.get_manager import MarketingManagerResponseGetSerializer
from pms_apps.marketing.serializers.response.get_all.get_all_manager import MarketingManagerResponseGetAllSerializer

from pms_apps.marketing.views.marketing_manager import MarketingManagerView


class MarketingManagerViewController:
    @extend_schema(
        description="Add a Marketing Manager",
        request=MarketingManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=MarketingManagerView().manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingManagerCreateRequestSerializer).validate
    def create_manager(request: Request) -> Response:
        return MarketingManagerView().create_manager_extract(params=request.params)

    @extend_schema(
        description="Update a Marketing Manager",
        request=MarketingManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=MarketingManagerView().manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return MarketingManagerView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a Marketing Manager",
        parameters=MarketingManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=MarketingManagerView().manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingManagerDeleteRequestSerializer).validate
    def delete_manager(request: Request) -> Response:
        return MarketingManagerView().delete_manager_extract(params=request.params)

    @extend_schema(
        description="Get a Marketing Manager",
        parameters=MarketingManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=MarketingManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingManagerGetRequestSerializer).validate
    def get_manager(request: Request) -> Response:
        print('ehre')
        return MarketingManagerView().get_manager_extract(params=request.params)

    @extend_schema(
        description="Get all Marketing Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=MarketingManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return MarketingManagerView().get_all_manager_extract(params=request.params)
