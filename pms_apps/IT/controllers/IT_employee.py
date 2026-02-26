from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.IT.serializers.request.create.create_employee import ITEmployeeCreateRequestSerializer
from pms_apps.IT.serializers.request.update.update_employee import ITEmployeeUpdateRequestSerializer
from pms_apps.IT.serializers.request.delete.delete_employee import ITEmployeeDeleteRequestSerializer
from pms_apps.IT.serializers.request.get.get_employee import ITEmployeeGetRequestSerializer
from pms_apps.IT.serializers.response.get.get_employee import ITEmployeeResponseGetSerializer
from pms_apps.IT.serializers.response.get_all.get_all_employee import ITEmployeeResponseGetAllSerializer
from pms_apps.IT.views.IT_employee import ITEmployeeView


class ITEmployeeViewController:
    @extend_schema(
        description="Add a IT Employee",
        request=ITEmployeeCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=ITEmployeeView().employee_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITEmployeeCreateRequestSerializer).validate
    def create_employee(request: Request) -> Response:
        return ITEmployeeView().create_employee_extract(params=request.params)

    @extend_schema(
        description="Update a IT Employee",
        request=ITEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=ITEmployeeView().employee_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return ITEmployeeView().update_employee_extract(params=request.params)

    @extend_schema(
        description="Delete a IT Employee",
        parameters=ITEmployeeDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=ITEmployeeView().employee_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITEmployeeDeleteRequestSerializer).validate
    def delete_employee(request: Request) -> Response:
        return ITEmployeeView().delete_employee_extract(params=request.params)

    @extend_schema(
        description="Get a IT Employee",
        parameters=ITEmployeeGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=ITEmployeeResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ITEmployeeGetRequestSerializer).validate
    def get_employee(request: Request) -> Response:
        return ITEmployeeView().get_employee_extract(params=request.params)

    @extend_schema(
        description="Get all IT Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=ITEmployeeResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return ITEmployeeView().get_all_employee_extract(params=request.params)
