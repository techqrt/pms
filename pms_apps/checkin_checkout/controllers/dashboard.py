from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializers.request.get_all import GetAllSerializer
from pms_apps.common.serializer_validations import SerializerValidations

from pms_apps.checkin_checkout.views.dashboard import MainDashboardView, CheckInDashboardView, CheckOutDashboardView


# noinspection PyMethodParameters
class DashboardViewController:

    @extend_schema(
        description="Get Main Dashboard Summary (stat cards, status overview, monthly overview)",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=MainDashboardView().data_summary)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def summary(request: Request) -> Response:
        return MainDashboardView().summary_extract(params=request.params)

    @extend_schema(
        description="Get Pending Settlements list for the Main Dashboard",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=MainDashboardView().data_pending_settlements)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def pending_settlements(request: Request) -> Response:
        return MainDashboardView().pending_settlements_extract(params=request.params)


# noinspection PyMethodParameters
class CheckInDashboardViewController:

    @extend_schema(
        description="Get Check-In Dashboard Summary (stat cards, status overview, property type, workflow funnel)",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckInDashboardView().data_summary)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def summary(request: Request) -> Response:
        return CheckInDashboardView().summary_extract(params=request.params)

    @extend_schema(
        description="Get Upcoming Check-Ins list for the Check-In Dashboard",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckInDashboardView().data_upcoming)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def upcoming(request: Request) -> Response:
        return CheckInDashboardView().upcoming_extract(params=request.params)


# noinspection PyMethodParameters
class CheckOutDashboardViewController:

    @extend_schema(
        description="Get Check-Out Dashboard Summary (stat cards, status overview, progress funnel)",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckOutDashboardView().data_summary)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def summary(request: Request) -> Response:
        return CheckOutDashboardView().summary_extract(params=request.params)

    @extend_schema(
        description="Get Upcoming Check-Outs list for the Check-Out Dashboard",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckOutDashboardView().data_upcoming)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def upcoming(request: Request) -> Response:
        return CheckOutDashboardView().upcoming_extract(params=request.params)

    @extend_schema(
        description="Get Check-Out Dashboard Widgets (financial overview, damage categories, utility overview, key return status)",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckOutDashboardView().data_widgets)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def widgets(request: Request) -> Response:
        return CheckOutDashboardView().widgets_extract(params=request.params)
