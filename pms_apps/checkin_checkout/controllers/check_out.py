from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.checkin_checkout.serializers.requests.create_check_out import CheckOutCreateSerializer
from pms_apps.checkin_checkout.serializers.requests.get_check_out import CheckOutGetSerializer
from pms_apps.checkin_checkout.serializers.requests.update_check_out import (
    CheckOutInformationUpdateSerializer,
    CheckOutTenantDetailsUpdateSerializer,
    CheckOutPropertyDetailsUpdateSerializer,
    CheckOutRentalDetailsUpdateSerializer,
    CheckOutPropertyInspectionUpdateSerializer,
    CheckOutRepairDamageUpdateSerializer,
    CheckOutUtilityMeterReadingsUpdateSerializer,
    CheckOutFinanceDetailsUpdateSerializer,
    CheckOutKeyReturnUpdateSerializer,
    CheckOutCommentsUpdateSerializer,
)
from pms_apps.checkin_checkout.serializers.response.get_check_out import CheckOutResponseGetSerializer
from pms_apps.checkin_checkout.serializers.response.get_all_check_out import CheckOutResponseGetAllSerializer
from pms_apps.checkin_checkout.views.check_out import CheckOutView

from pms_apps.common.serializer_validations import SerializerValidations


# noinspection PyMethodParameters
class CheckOutViewController:

    @extend_schema(
        description="Create a Check-Out",
        request=CheckOutCreateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_create)
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckOutCreateSerializer).validate
    def create(request: Request) -> Response:
        return CheckOutView().create_extract(params=request.params)

    @extend_schema(
        description="Get a single Check-Out",
        parameters=CheckOutGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=CheckOutView().data_get, response=CheckOutResponseGetSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=CheckOutGetSerializer).validate
    def get(request: Request) -> Response:
        return CheckOutView().get_extract(params=request.params)

    @extend_schema(
        description="Get all Check-Outs",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckOutView().data_get, response=CheckOutResponseGetAllSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return CheckOutView().get_all_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Information (Section A)",
        request=CheckOutInformationUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutInformationUpdateSerializer).validate
    def update_information(request: Request) -> Response:
        return CheckOutView().update_information_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Tenant Details (Section B)",
        request=CheckOutTenantDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutTenantDetailsUpdateSerializer).validate
    def update_tenant_details(request: Request) -> Response:
        return CheckOutView().update_tenant_details_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Property Details (Section C)",
        request=CheckOutPropertyDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutPropertyDetailsUpdateSerializer).validate
    def update_property_details(request: Request) -> Response:
        return CheckOutView().update_property_details_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Rental Details (Section D)",
        request=CheckOutRentalDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutRentalDetailsUpdateSerializer).validate
    def update_rental_details(request: Request) -> Response:
        return CheckOutView().update_rental_details_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Property Inspection (Section E)",
        request=CheckOutPropertyInspectionUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutPropertyInspectionUpdateSerializer).validate
    def update_property_inspection(request: Request) -> Response:
        return CheckOutView().update_property_inspection_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Repair & Damage (Section F)",
        request=CheckOutRepairDamageUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutRepairDamageUpdateSerializer).validate
    def update_repair_damage(request: Request) -> Response:
        return CheckOutView().update_repair_damage_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Utility Meter Readings (Section G)",
        request=CheckOutUtilityMeterReadingsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutUtilityMeterReadingsUpdateSerializer).validate
    def update_utility_meter_readings(request: Request) -> Response:
        return CheckOutView().update_utility_meter_readings_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Finance Details (Section H)",
        request=CheckOutFinanceDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutFinanceDetailsUpdateSerializer).validate
    def update_finance_details(request: Request) -> Response:
        return CheckOutView().update_finance_details_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Key Return (Section I)",
        request=CheckOutKeyReturnUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutKeyReturnUpdateSerializer).validate
    def update_key_return(request: Request) -> Response:
        return CheckOutView().update_key_return_extract(params=request.params)

    @extend_schema(
        description="Update Check-Out Comments (Section K)",
        request=CheckOutCommentsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutCommentsUpdateSerializer).validate
    def update_comments(request: Request) -> Response:
        return CheckOutView().update_comments_extract(params=request.params)
