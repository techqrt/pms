from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.collection.serializers.request.create.create_manager import CollectionManagerCreateRequestSerializer
from pms_apps.collection.serializers.request.update.update_manager import CollectionManagerUpdateRequestSerializer
from pms_apps.collection.serializers.request.delete.delete_manager import CollectionManagerDeleteRequestSerializer
from pms_apps.collection.serializers.request.get.get_manager import CollectionManagerGetRequestSerializer
from pms_apps.collection.serializers.response.get.get_manager import CollectionManagerResponseGetSerializer
from pms_apps.collection.serializers.response.get_all.get_all_manager import CollectionManagerResponseGetAllSerializer
from pms_apps.collection.views.collection_manager import CollectionManagerView

class CollectionManagerViewController:
    @extend_schema(
        description="Add a Collection Manager",
        request=CollectionManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=CollectionManagerView().manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionManagerCreateRequestSerializer).validate
    def create_manager(request: Request) -> Response:
        return CollectionManagerView().create_manager_extract(params=request.params)

    @extend_schema(
        description="Update a Collection Manager",
        request=CollectionManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=CollectionManagerView().manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return CollectionManagerView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a Collection Manager",
        parameters=CollectionManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=CollectionManagerView().manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionManagerDeleteRequestSerializer).validate
    def delete_manager(request: Request) -> Response:
        return CollectionManagerView().delete_manager_extract(params=request.params)

    @extend_schema(
        description="Get a Collection Manager",
        parameters=CollectionManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=CollectionManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionManagerGetRequestSerializer).validate
    def get_manager(request: Request) -> Response:
        return CollectionManagerView().get_manager_extract(params=request.params)

    @extend_schema(
        description="Get all Collection Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=CollectionManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return CollectionManagerView().get_all_manager_extract(params=request.params)
