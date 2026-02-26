from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.finance.serializers.request.create.create_manager import FinanceManagerCreateRequestSerializer
from pms_apps.finance.serializers.request.update.update_manager import FinanceManagerUpdateRequestSerializer
from pms_apps.finance.serializers.request.delete.delete_manager import FinanceManagerDeleteRequestSerializer
from pms_apps.finance.serializers.request.get.get_manager import FinanceManagerGetRequestSerializer
from pms_apps.finance.serializers.response.get.get_manager import FinanceManagerResponseGetSerializer
from pms_apps.finance.serializers.response.get_all.get_all_manager import FinanceManagerResponseGetAllSerializer
from pms_apps.finance.views.finance_manager import FinanceManagerView

class FinanceManagerViewController:
    @extend_schema(
        description="Add a Finance Manager",
        request=FinanceManagerCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=FinanceManagerView().manager_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceManagerCreateRequestSerializer).validate
    def create_manager(request: Request) -> Response:
        return FinanceManagerView().create_manager_extract(params=request.params)

    @extend_schema(
        description="Update a Finance Manager",
        request=FinanceManagerUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=FinanceManagerView().manager_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceManagerUpdateRequestSerializer).validate
    def update_manager(request: Request) -> Response:
        return FinanceManagerView().update_manager_extract(params=request.params)

    @extend_schema(
        description="Delete a Finance Manager",
        parameters=FinanceManagerDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=FinanceManagerView().manager_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceManagerDeleteRequestSerializer).validate
    def delete_manager(request: Request) -> Response:
        return FinanceManagerView().delete_manager_extract(params=request.params)

    @extend_schema(
        description="Get a Finance Manager",
        parameters=FinanceManagerGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=FinanceManagerResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceManagerGetRequestSerializer).validate
    def get_manager(request: Request) -> Response:
        return FinanceManagerView().get_manager_extract(params=request.params)

    @extend_schema(
        description="Get all Finance Managers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=FinanceManagerResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_manager(request: Request) -> Response:
        return FinanceManagerView().get_all_manager_extract(params=request.params)
