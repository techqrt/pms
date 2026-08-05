from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
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
from pms_apps.property.serializers.requests.property_assignment_create import PropertyAssignmentCreateSerializer
from pms_apps.property.serializers.requests.property_assignment_update import PropertyAssignmentUpdateSerializer
from pms_apps.property.serializers.requests.property_assignment_get import PropertyAssignmentGetSerializer
from pms_apps.property.serializers.requests.occupancy_report import OccupancyReportSerializer

from pms_apps.property.serializers.response.get import PropertyResponseGetSerializer
from pms_apps.property.serializers.response.get_all import PropertyResponseGetAllSerializer
from pms_apps.property.views import PropertyView


# noinspection PyMethodParameters
class PropertyViewController:


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


    @extend_schema(
        description="Get a Property by ID",
        parameters=PropertyGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=PropertyResponseGetSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=PropertyGetSerializer).validate
    def get(request: Request) -> Response:
        return PropertyView().get_extract(params=request.params)


    @extend_schema(
        description="Get all Properties (Paginated)",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=PropertyResponseGetAllSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return PropertyView().get_all_extract(params=request.params)


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

    @extend_schema(
        description="Get total count of Properties",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description="Total properties count")
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def count(request: Request) -> Response:
        return PropertyView().count_extract(params=request.params)

    @extend_schema(
        description="Get Occupancy Summary - Total, Rented, Vacant, and Booked properties",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=PropertyView().data_occupancy_summary)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def occupancy_summary(request: Request) -> Response:
        return PropertyView().occupancy_summary_extract(params=request.params)

    @extend_schema(
        description="Get Occupancy Report list (Paginated) - filter by search, property_types, statuses, date range",
        parameters=[
            OpenApiParameter(name='page_num', required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='limit', required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='search', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='property_types', description='Comma separated: Apartment,Villa,Warehouse,Commercial',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='statuses', description='Comma separated: Vacant,Booked,Rented,Under Maintenance',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='from_date', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='to_date', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ],
        responses=SwaggerPage.response(description=PropertyView().data_occupancy_list)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=OccupancyReportSerializer).validate
    def occupancy_list(request: Request) -> Response:
        return PropertyView().occupancy_list_extract(params=request.params)

    @extend_schema(
        description="Assign Property to Tenant with Full Details",
        request=PropertyAssignmentCreateSerializer,
        responses=SwaggerPage.response(description=PropertyView().data_assign)
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=PropertyAssignmentCreateSerializer).validate
    def assign(request: Request) -> Response:
        return PropertyView().assign_extract(params=request.params)

    @extend_schema(
        description="Update a Property Assignment",
        request=PropertyAssignmentUpdateSerializer,
        responses=SwaggerPage.response(description=PropertyView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=PropertyAssignmentUpdateSerializer).validate
    def update_assignment(request: Request) -> Response:
        return PropertyView().update_assignment_extract(params=request.params)

    @extend_schema(
        description="Get Single Property Assignment",
        parameters=PropertyAssignmentGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=PropertyView().data_get)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=PropertyAssignmentGetSerializer).validate
    def get_assignment(request: Request) -> Response:
        return PropertyView().get_extract_assignment(params=request.params)

    @extend_schema(
        description="Get All Property Assignments",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=PropertyView().data_get)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all_assignments(request: Request) -> Response:
        return PropertyView().get_all_extract_assignment(params=request.params)

    @extend_schema(
        description="Get Assignment Count - Total, Assigned, and Unassigned Properties",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=PropertyView().data_assignment_count)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def assignment_count(request: Request) -> Response:
        return PropertyView().assignment_count_extract(params=request.params)
