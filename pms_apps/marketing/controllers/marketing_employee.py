from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.marketing.serializers.request.create.create_employee import MarketingEmployeeCreateRequestSerializer
from pms_apps.marketing.serializers.request.update.update_employee import MarketingEmployeeUpdateRequestSerializer
from pms_apps.marketing.serializers.request.delete.delete_employee import MarketingEmployeeDeleteRequestSerializer
from pms_apps.marketing.serializers.request.get.get_employee import MarketingEmployeeGetRequestSerializer
from pms_apps.marketing.serializers.response.get.get_employee import MarketingEmployeeResponseGetSerializer
from pms_apps.marketing.serializers.response.get_all.get_all_employee import MarketingEmployeeResponseGetAllSerializer

from pms_apps.marketing.views.marketing_employee import MarketingEmployeeView


class MarketingEmployeeViewController:
    @extend_schema(
        description="Add a Marketing Employee",
        request=MarketingEmployeeCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=MarketingEmployeeView().employee_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingEmployeeCreateRequestSerializer).validate
    def create_employee(request: Request) -> Response:
        return MarketingEmployeeView().create_employee_extract(params=request.params)

    @extend_schema(
        description="Update a Marketing Employee",
        request=MarketingEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=MarketingEmployeeView().employee_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return MarketingEmployeeView().update_employee_extract(params=request.params)

    @extend_schema(
        description="Delete a Marketing Employee",
        parameters=MarketingEmployeeDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=MarketingEmployeeView().employee_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingEmployeeDeleteRequestSerializer).validate
    def delete_employee(request: Request) -> Response:
        return MarketingEmployeeView().delete_employee_extract(params=request.params)

    @extend_schema(
        description="Get a Marketing Employee",
        parameters=MarketingEmployeeGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=MarketingEmployeeResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingEmployeeGetRequestSerializer).validate
    def get_employee(request: Request) -> Response:
        return MarketingEmployeeView().get_employee_extract(params=request.params)

    @extend_schema(
        description="Get all Marketing Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=MarketingEmployeeResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return MarketingEmployeeView().get_all_employee_extract(params=request.params)
