from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.collection.serializers.request.create.create_employee import CollectionEmployeeCreateRequestSerializer
from pms_apps.collection.serializers.request.update.update_employee import CollectionEmployeeUpdateRequestSerializer
from pms_apps.collection.serializers.request.delete.delete_employee import CollectionEmployeeDeleteRequestSerializer
from pms_apps.collection.serializers.request.get.get_employee import CollectionEmployeeGetRequestSerializer
from pms_apps.collection.serializers.response.get.get_employee import CollectionEmployeeResponseGetSerializer
from pms_apps.collection.serializers.response.get_all.get_all_employee import CollectionEmployeeResponseGetAllSerializer
from pms_apps.collection.views.collection_employee import CollectionEmployeeView


class CollectionEmployeeViewController:
    @extend_schema(
        description="Add a Collection Employee",
        request=CollectionEmployeeCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=CollectionEmployeeView().employee_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionEmployeeCreateRequestSerializer).validate
    def create_employee(request: Request) -> Response:
        return CollectionEmployeeView().create_employee_extract(params=request.params)

    @extend_schema(
        description="Update a Collection Employee",
        request=CollectionEmployeeUpdateRequestSerializer,
        responses=SwaggerPage.response(
            description=CollectionEmployeeView().employee_update)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionEmployeeUpdateRequestSerializer).validate
    def update_employee(request: Request) -> Response:
        return CollectionEmployeeView().update_employee_extract(params=request.params)

    @extend_schema(
        description="Delete a Collection Employee",
        parameters=CollectionEmployeeDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            description=CollectionEmployeeView().employee_delete)
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionEmployeeDeleteRequestSerializer).validate
    def delete_employee(request: Request) -> Response:
        return CollectionEmployeeView().delete_employee_extract(params=request.params)

    @extend_schema(
        description="Get a Collection Employee",
        parameters=CollectionEmployeeGetRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=CollectionEmployeeResponseGetSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=CollectionEmployeeGetRequestSerializer).validate
    def get_employee(request: Request) -> Response:
        return CollectionEmployeeView().get_employee_extract(params=request.params)

    @extend_schema(
        description="Get all Collection Employees",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(
            response=CollectionEmployeeResponseGetAllSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_employee(request: Request) -> Response:
        return CollectionEmployeeView().get_all_employee_extract(params=request.params)
