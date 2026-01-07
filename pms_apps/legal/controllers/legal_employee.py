from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.legal.serializers.request.create.create_employee import LegalEmployeeCreateRequestSerializer
from pms_apps.legal.serializers.request.update.update_employee import LegalEmployeeUpdateRequestSerializer
from pms_apps.legal.serializers.request.delete.delete_employee import LegalEmployeeDeleteRequestSerializer
from pms_apps.legal.serializers.request.get.get_employee import LegalEmployeeGetRequestSerializer
from pms_apps.legal.serializers.response.get.get_employee import LegalEmployeeResponseGetSerializer
from pms_apps.legal.serializers.response.get_all.get_all_employee import LegalEmployeeResponseGetAllSerializer
from pms_apps.legal.views.legal_employee import LegalEmployeeView


class LegalEmployeeViewController:
    @extend_schema(
        description="Add a Legal Employee",
        request=LegalEmployeeCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=LegalEmployeeView().employee_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalEmployeeCreateRequestSerializer).validate
    def create_employee(request: Request) -> Response:
        return LegalEmployeeView().create_employee_extract(params=request.params)

    @extend_schema(
        description="Update a Legal Employee",
        request=LegalEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=LegalEmployeeView().employee_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return LegalEmployeeView().update_employee_extract(params=request.params)

    @extend_schema(
        description="Delete a Legal Employee",
        parameters=LegalEmployeeDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=LegalEmployeeView().employee_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalEmployeeDeleteRequestSerializer).validate
    def delete_employee(request: Request) -> Response:
        return LegalEmployeeView().delete_employee_extract(params=request.params)

    @extend_schema(
        description="Get a Legal Employee",
        parameters=LegalEmployeeGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=LegalEmployeeResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=LegalEmployeeGetRequestSerializer).validate
    def get_employee(request: Request) -> Response:
        return LegalEmployeeView().get_employee_extract(params=request.params)

    @extend_schema(
        description="Get all Legal Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=LegalEmployeeResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return LegalEmployeeView().get_all_employee_extract(params=request.params)
