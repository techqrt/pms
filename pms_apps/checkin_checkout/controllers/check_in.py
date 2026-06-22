from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializers.request.get_all import GetAllSerializer

from pms_apps.checkin_checkout.serializers.requests.create_check_in import CheckInCreateSerializer
from pms_apps.checkin_checkout.serializers.requests.get_check_in import CheckInGetSerializer
from pms_apps.checkin_checkout.serializers.requests.update_check_in import (
    CheckInInformationUpdateSerializer,
    CheckInTenantDetailsUpdateSerializer,
    CheckInPropertyDetailsUpdateSerializer,
    CheckInRentalDetailsUpdateSerializer,
    CheckInPropertyInspectionUpdateSerializer,
    CheckInRepairApprovalUpdateSerializer,
    CheckInUtilityMeterReadingsUpdateSerializer,
    CheckInAgreementDetailsUpdateSerializer,
    CheckInKeyHandoverUpdateSerializer,
    CheckInCommentsUpdateSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.upload_check_in_document import CheckInDocumentUploadSerializer
from pms_apps.checkin_checkout.serializers.requests.create_check_in_inspection_item import (
    CheckInInspectionItemCreateSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.update_check_in_inspection_item import (
    CheckInInspectionItemUpdateSerializer,
    CheckInInspectionItemDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.create_check_in_utility_reading import (
    CheckInUtilityReadingCreateSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.update_check_in_utility_reading import (
    CheckInUtilityReadingUpdateSerializer,
    CheckInUtilityReadingDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.create_check_in_payment import (
    CheckInPaymentCreateSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.update_check_in_payment import (
    CheckInPaymentUpdateSerializer,
    CheckInPaymentDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.create_check_in_key import (
    CheckInKeyCreateSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.update_check_in_key import (
    CheckInKeyUpdateSerializer,
    CheckInKeyDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.delete_check_in import CheckInDeleteSerializer
from pms_apps.checkin_checkout.serializers.response.get import CheckInResponseGetSerializer
from pms_apps.checkin_checkout.serializers.response.get_all import CheckInResponseGetAllSerializer
from pms_apps.checkin_checkout.views.check_in import CheckInView

from pms_apps.common.serializer_validations import SerializerValidations


# noinspection PyMethodParameters
class CheckInViewController:

    @extend_schema(
        description="Create a Check-In",
        request=CheckInCreateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_create)
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckInCreateSerializer).validate
    def create(request: Request) -> Response:
        return CheckInView().create_extract(params=request.params)

    @extend_schema(
        description="Get a single Check-In",
        parameters=CheckInGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=CheckInView().data_get, response=CheckInResponseGetSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=CheckInGetSerializer).validate
    def get(request: Request) -> Response:
        return CheckInView().get_extract(params=request.params)

    @extend_schema(
        description="Get all Check-Ins",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(description=CheckInView().data_get, response=CheckInResponseGetAllSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return CheckInView().get_all_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-In",
        parameters=CheckInDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=CheckInView().data_delete)
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckInDeleteSerializer).validate
    def delete(request: Request) -> Response:
        return CheckInView().delete_extract(params=request.params)

    @extend_schema(
        description="Update Check-In Information (Section A)",
        request=CheckInInformationUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInInformationUpdateSerializer).validate
    def update_information(request: Request) -> Response:
        return CheckInView().update_information_extract(params=request.params)

    @extend_schema(
        description="Update Tenant Details (Section B)",
        request=CheckInTenantDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInTenantDetailsUpdateSerializer).validate
    def update_tenant_details(request: Request) -> Response:
        return CheckInView().update_tenant_details_extract(params=request.params)

    @extend_schema(
        description="Update Property Details (Section C)",
        request=CheckInPropertyDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInPropertyDetailsUpdateSerializer).validate
    def update_property_details(request: Request) -> Response:
        return CheckInView().update_property_details_extract(params=request.params)

    @extend_schema(
        description="Update Rental Details (Section D)",
        request=CheckInRentalDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInRentalDetailsUpdateSerializer).validate
    def update_rental_details(request: Request) -> Response:
        return CheckInView().update_rental_details_extract(params=request.params)

    @extend_schema(
        description="Update Property Inspection (Section E)",
        request=CheckInPropertyInspectionUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInPropertyInspectionUpdateSerializer).validate
    def update_property_inspection(request: Request) -> Response:
        return CheckInView().update_property_inspection_extract(params=request.params)

    @extend_schema(
        description="Update Repair & Approval (Section F)",
        request=CheckInRepairApprovalUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInRepairApprovalUpdateSerializer).validate
    def update_repair_approval(request: Request) -> Response:
        return CheckInView().update_repair_approval_extract(params=request.params)

    @extend_schema(
        description="Update Utility Meter Readings (Section G)",
        request=CheckInUtilityMeterReadingsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInUtilityMeterReadingsUpdateSerializer).validate
    def update_utility_meter_readings(request: Request) -> Response:
        return CheckInView().update_utility_meter_readings_extract(params=request.params)

    @extend_schema(
        description="Update Agreement Details (Section H)",
        request=CheckInAgreementDetailsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInAgreementDetailsUpdateSerializer).validate
    def update_agreement_details(request: Request) -> Response:
        return CheckInView().update_agreement_details_extract(params=request.params)

    @extend_schema(
        description="Update Key Handover (Section I)",
        request=CheckInKeyHandoverUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInKeyHandoverUpdateSerializer).validate
    def update_key_handover(request: Request) -> Response:
        return CheckInView().update_key_handover_extract(params=request.params)

    @extend_schema(
        description="Update Comments (Section K)",
        request=CheckInCommentsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckInView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInCommentsUpdateSerializer).validate
    def update_comments(request: Request) -> Response:
        return CheckInView().update_comments_extract(params=request.params)

    @extend_schema(
        description="Upload a Check-In Document (Section J)",
        request=CheckInDocumentUploadSerializer,
        responses=SwaggerPage.response(description="Document uploaded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckInDocumentUploadSerializer).validate
    def upload_document(request: Request) -> Response:
        return CheckInView().upload_document_extract(params=request.params)

    @extend_schema(
        description="Create a Check-In Inspection Item",
        request=CheckInInspectionItemCreateSerializer,
        responses=SwaggerPage.response(description="Inspection item recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckInInspectionItemCreateSerializer).validate
    def create_inspection_item(request: Request) -> Response:
        return CheckInView().create_inspection_item_extract(params=request.params)

    @extend_schema(
        description="Update a Check-In Inspection Item",
        request=CheckInInspectionItemUpdateSerializer,
        responses=SwaggerPage.response(description="Inspection item updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInInspectionItemUpdateSerializer).validate
    def update_inspection_item(request: Request) -> Response:
        return CheckInView().update_inspection_item_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-In Inspection Item",
        parameters=CheckInInspectionItemDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Inspection item deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckInInspectionItemDeleteSerializer).validate
    def delete_inspection_item(request: Request) -> Response:
        return CheckInView().delete_inspection_item_extract(params=request.params)

    @extend_schema(
        description="Create a Check-In Utility Reading",
        request=CheckInUtilityReadingCreateSerializer,
        responses=SwaggerPage.response(description="Utility reading recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckInUtilityReadingCreateSerializer).validate
    def create_utility_reading(request: Request) -> Response:
        return CheckInView().create_utility_reading_extract(params=request.params)

    @extend_schema(
        description="Update a Check-In Utility Reading",
        request=CheckInUtilityReadingUpdateSerializer,
        responses=SwaggerPage.response(description="Utility reading updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInUtilityReadingUpdateSerializer).validate
    def update_utility_reading(request: Request) -> Response:
        return CheckInView().update_utility_reading_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-In Utility Reading",
        parameters=CheckInUtilityReadingDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Utility reading deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckInUtilityReadingDeleteSerializer).validate
    def delete_utility_reading(request: Request) -> Response:
        return CheckInView().delete_utility_reading_extract(params=request.params)

    @extend_schema(
        description="Create a Check-In Payment",
        request=CheckInPaymentCreateSerializer,
        responses=SwaggerPage.response(description="Payment recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckInPaymentCreateSerializer).validate
    def create_payment(request: Request) -> Response:
        return CheckInView().create_payment_extract(params=request.params)

    @extend_schema(
        description="Update a Check-In Payment",
        request=CheckInPaymentUpdateSerializer,
        responses=SwaggerPage.response(description="Payment updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInPaymentUpdateSerializer).validate
    def update_payment(request: Request) -> Response:
        return CheckInView().update_payment_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-In Payment",
        parameters=CheckInPaymentDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Payment deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckInPaymentDeleteSerializer).validate
    def delete_payment(request: Request) -> Response:
        return CheckInView().delete_payment_extract(params=request.params)

    @extend_schema(
        description="Create a Check-In Key",
        request=CheckInKeyCreateSerializer,
        responses=SwaggerPage.response(description="Key recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckInKeyCreateSerializer).validate
    def create_key(request: Request) -> Response:
        return CheckInView().create_key_extract(params=request.params)

    @extend_schema(
        description="Update a Check-In Key",
        request=CheckInKeyUpdateSerializer,
        responses=SwaggerPage.response(description="Key updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckInKeyUpdateSerializer).validate
    def update_key(request: Request) -> Response:
        return CheckInView().update_key_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-In Key",
        parameters=CheckInKeyDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Key deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckInKeyDeleteSerializer).validate
    def delete_key(request: Request) -> Response:
        return CheckInView().delete_key_extract(params=request.params)
