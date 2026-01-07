from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.finance.serializers.request.create.create_employee import FinanceEmployeeCreateRequestSerializer
from pms_apps.finance.serializers.request.update.update_employee import FinanceEmployeeUpdateRequestSerializer
from pms_apps.finance.serializers.request.delete.delete_employee import FinanceEmployeeDeleteRequestSerializer
from pms_apps.finance.serializers.request.get.get_employee import FinanceEmployeeGetRequestSerializer
from pms_apps.finance.serializers.response.get.get_employee import FinanceEmployeeResponseGetSerializer
from pms_apps.finance.serializers.response.get_all.get_all_employee import FinanceEmployeeResponseGetAllSerializer
from pms_apps.finance.views.finance_employee import FinanceEmployeeView


class FinanceEmployeeViewController:
    @extend_schema(
        description="Add a Finance Employee",
        request=FinanceEmployeeCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=FinanceEmployeeView().employee_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceEmployeeCreateRequestSerializer).validate
    def create_employee(request: Request) -> Response:
        return FinanceEmployeeView().create_employee_extract(params=request.params)

    @extend_schema(
        description="Update a Finance Employee",
        request=FinanceEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=FinanceEmployeeView().employee_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return FinanceEmployeeView().update_employee_extract(params=request.params)

    @extend_schema(
        description="Delete a Finance Employee",
        parameters=FinanceEmployeeDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=FinanceEmployeeView().employee_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceEmployeeDeleteRequestSerializer).validate
    def delete_employee(request: Request) -> Response:
        return FinanceEmployeeView().delete_employee_extract(params=request.params)

    @extend_schema(
        description="Get a Finance Employee",
        parameters=FinanceEmployeeGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=FinanceEmployeeResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=FinanceEmployeeGetRequestSerializer).validate
    def get_employee(request: Request) -> Response:
        return FinanceEmployeeView().get_employee_extract(params=request.params)

    @extend_schema(
        description="Get all Finance Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=FinanceEmployeeResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return FinanceEmployeeView().get_all_employee_extract(params=request.params)
