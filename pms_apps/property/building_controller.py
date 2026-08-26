from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.common.serializers.request.get_all import GetAllSerializer
from pms_apps.common.swagger import SwaggerPage

from pms_apps.property.serializers.requests.building_create import BuildingCreateSerializer
from pms_apps.property.serializers.requests.building_update import BuildingUpdateSerializer
from pms_apps.property.serializers.requests.building_delete import BuildingDeleteSerializer
from pms_apps.property.serializers.requests.building_get import BuildingGetSerializer

from pms_apps.property.serializers.response.building_get import BuildingResponseGetSerializer
from pms_apps.property.serializers.response.building_get_all import BuildingResponseGetAllSerializer
from pms_apps.property.building_views import BuildingView


# noinspection PyMethodParameters
class BuildingViewController:

    @extend_schema(
        description="Add a Building",
        request=BuildingCreateSerializer,
        responses=SwaggerPage.response(description=BuildingView().data_create)
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=BuildingCreateSerializer,
                           exec_func="BuildingView().create_extract(request)").validate
    def create(request: Request) -> Response:
        return BuildingView().create_extract(params=request.params)

    @extend_schema(
        description="Update a Building",
        request=BuildingUpdateSerializer,
        responses=SwaggerPage.response(description=BuildingView().data_update)
    )
    @api_view(["PUT"])
    @SerializerValidations(serializer=BuildingUpdateSerializer,
                           exec_func="BuildingView().update_extract(request)").validate
    def update(request: Request) -> Response:
        return BuildingView().update_extract(params=request.params)

    @extend_schema(
        description="Delete a Building",
        parameters=BuildingDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=BuildingView().data_delete)
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=BuildingDeleteSerializer,
                           exec_func="BuildingView().delete_extract(request)").validate
    def delete(request: Request) -> Response:
        return BuildingView().delete_extract(params=request.params)

    @extend_schema(
        description="Get a Building by ID",
        parameters=BuildingGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=BuildingResponseGetSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=BuildingGetSerializer).validate
    def get(request: Request) -> Response:
        return BuildingView().get_extract(params=request.params)

    @extend_schema(
        description="Get all Buildings (Paginated) - filter by search_key",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=BuildingResponseGetAllSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return BuildingView().get_all_extract(params=request.params)
