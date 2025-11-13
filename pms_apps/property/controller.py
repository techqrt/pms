from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer
from pms_apps.common.swagger import SwaggerPage

from pms_apps.property.serializers.requests.create import PropertyCreateSerializer
from pms_apps.property.serializers.requests.update import PropertyUpdateSerializer
from pms_apps.property.serializers.requests.delete import PropertyDeleteSerializer
from pms_apps.property.serializers.requests.delete_many import PropertyDeleteManySerializer
from pms_apps.property.serializers.requests.get import PropertyGetSerializer

from pms_apps.property.serializers.response.get import PropertyGetResponseSerializer
from pms_apps.property.serializers.response.get_all import PropertyGetAllResponseSerializer
from pms_apps.property.views import PropertyView


# noinspection PyMethodParameters
class PropertyViewController:

    # -------------------------------
    # CREATE PROPERTY
    # -------------------------------
    @extend_schema(
        description="Add a Property",
        request=PropertyCreateSerializer,
        responses=SwaggerPage.response(description=PropertyView().data_create)
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=PropertyCreateSerializer,
                           exec_func="PropertyView().create_extract(request)").validate
    def create(request: Request) -> Response:
        return PropertyView().create_extract(params=request.params)

    # -------------------------------
    # UPDATE PROPERTY
    # -------------------------------
    @extend_schema(
        description="Update a Property",
        request=PropertyUpdateSerializer,
        responses=SwaggerPage.response(description=PropertyView().data_update)
    )
    @api_view(["PUT"])
    @SerializerValidations(serializer=PropertyUpdateSerializer,
                           exec_func="PropertyView().update_extract(request)").validate
    def update(request: Request) -> Response:
        return PropertyView().update_extract(params=request.params)

    # -------------------------------
    # DELETE PROPERTY
    # -------------------------------
    @extend_schema(
        description="Delete a Property",
        parameters=PropertyDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=PropertyView().data_delete)
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=PropertyDeleteSerializer,
                           exec_func="PropertyView().delete_extract(request)").validate
    def delete(request: Request) -> Response:
        return PropertyView().delete_extract(params=request.params)

    # -------------------------------
    # GET SINGLE PROPERTY
    # -------------------------------
    @extend_schema(
        description="Get a Property by ID",
        parameters=PropertyGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=PropertyGetResponseSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=PropertyGetSerializer).validate
    def get(request: Request) -> Response:
        return PropertyView().get_extract(params=request.params)

    # -------------------------------
    # GET ALL PROPERTIES
    # -------------------------------
    @extend_schema(
        description="Get all Properties (Paginated)",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=PropertyGetAllResponseSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return PropertyView().get_all_extract(params=request.params)

    # -------------------------------
    # DELETE MULTIPLE PROPERTIES
    # -------------------------------
    @extend_schema(
        description="Delete multiple Properties",
        request=PropertyDeleteManySerializer,
        responses=SwaggerPage.response(description=PropertyView().data_delete)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=PropertyDeleteManySerializer,
                           exec_func="PropertyView().delete_many_extract(request)").validate
    def delete_many(request: Request) -> Response:
        return PropertyView().delete_many_extract(params=request.params)
