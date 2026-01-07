from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.reception.serializers.request.create.create_employee import ReceptionEmployeeCreateRequestSerializer
from pms_apps.reception.serializers.request.update.update_employee import ReceptionEmployeeUpdateRequestSerializer
from pms_apps.reception.serializers.request.delete.delete_employee import ReceptionEmployeeDeleteRequestSerializer
from pms_apps.reception.serializers.request.get.get_employee import ReceptionEmployeeGetRequestSerializer
from pms_apps.reception.serializers.response.get.get_employee import ReceptionEmployeeResponseGetSerializer
from pms_apps.reception.serializers.response.get_all.get_all_employee import ReceptionEmployeeResponseGetAllSerializer
from pms_apps.reception.views.reception_employee import ReceptionEmployeeView


class ReceptionEmployeeViewController:
    @extend_schema(
        description="Add a Reception Employee",
        request=ReceptionEmployeeCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=ReceptionEmployeeView().employee_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionEmployeeCreateRequestSerializer).validate
    def create_employee(request: Request) -> Response:
        return ReceptionEmployeeView().create_employee_extract(params=request.params)

    @extend_schema(
        description="Update a Reception Employee",
        request=ReceptionEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=ReceptionEmployeeView().employee_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return ReceptionEmployeeView().update_employee_extract(params=request.params)

    @extend_schema(
        description="Delete a Reception Employee",
        parameters=ReceptionEmployeeDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=ReceptionEmployeeView().employee_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionEmployeeDeleteRequestSerializer).validate
    def delete_employee(request: Request) -> Response:
        return ReceptionEmployeeView().delete_employee_extract(params=request.params)

    @extend_schema(
        description="Get a Reception Employee",
        parameters=ReceptionEmployeeGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=ReceptionEmployeeResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=ReceptionEmployeeGetRequestSerializer).validate
    def get_employee(request: Request) -> Response:
        return ReceptionEmployeeView().get_employee_extract(params=request.params)

    @extend_schema(
        description="Get all Reception Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=ReceptionEmployeeResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return ReceptionEmployeeView().get_all_employee_extract(params=request.params)
