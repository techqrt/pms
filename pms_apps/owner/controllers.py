from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.owner.serializers.request.create import OwnerCreateRequestSerializer
from pms_apps.owner.serializers.request.update import OwnerUpdateRequestSerializer
from pms_apps.owner.serializers.request.delete import OwnerDeleteRequestSerializer
from pms_apps.owner.serializers.request.get import OwnerGetRequestSerializer
from pms_apps.owner.serializers.response.get import OwnerResponseGetSerializer
from pms_apps.owner.serializers.response.get_all import OwnerResponseGetAllSerializer
from pms_apps.owner.views import OwnerView

class OwnerViewController:
    @extend_schema(
        description="Add a Owner",
        request=OwnerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=OwnerView().owner_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=OwnerCreateRequestSerializer).validate
    def create_owner(request: Request) -> Response:
        return OwnerView().create_owner_extract(params=request.params)

    @extend_schema(
        description="Update a Owner",
        request=OwnerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=OwnerView().owner_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=OwnerUpdateRequestSerializer).validate
    def update_owner(request: Request) -> Response:
        return OwnerView().update_owner_extract(params=request.params)

    @extend_schema(
        description="Delete a Owner",
        parameters=OwnerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=OwnerView().owner_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=OwnerDeleteRequestSerializer).validate
    def delete_owner(request: Request) -> Response:
        return OwnerView().delete_owner_extract(params=request.params)

    @extend_schema(
        description="Get a Owner",
        parameters=OwnerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=OwnerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=OwnerGetRequestSerializer).validate
    def get_owner(request: Request) -> Response:
        return OwnerView().get_owner_extract(params=request.params)

    @extend_schema(
        description="Get all Owners",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=OwnerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_owner(request: Request) -> Response:
        return OwnerView().get_all_owner_extract(params=request.params)
