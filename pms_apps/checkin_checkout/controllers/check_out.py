from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pms_apps.common.swagger import SwaggerPage

from pms_apps.checkin_checkout.serializers.requests.get_all_check_out import CheckOutGetAllSerializer
from pms_apps.checkin_checkout.serializers.requests.create_check_out import CheckOutCreateSerializer
from pms_apps.checkin_checkout.serializers.requests.get_check_out import CheckOutGetSerializer
from pms_apps.checkin_checkout.serializers.requests.delete_check_out import CheckOutDeleteSerializer
from pms_apps.checkin_checkout.serializers.requests.upload_check_out_document import CheckOutDocumentUploadSerializer
from pms_apps.checkin_checkout.serializers.requests.update_check_out_document import (
    CheckOutDocumentUpdateSerializer,
    CheckOutDocumentDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.create_check_out_inspection_item import CheckOutInspectionItemCreateSerializer
from pms_apps.checkin_checkout.serializers.requests.update_check_out_inspection_item import (
    CheckOutInspectionItemUpdateSerializer,
    CheckOutInspectionItemDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.create_check_out_utility_reading import CheckOutUtilityReadingCreateSerializer
from pms_apps.checkin_checkout.serializers.requests.update_check_out_utility_reading import (
    CheckOutUtilityReadingUpdateSerializer,
    CheckOutUtilityReadingDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.create_check_out_payment import CheckOutPaymentCreateSerializer
from pms_apps.checkin_checkout.serializers.requests.update_check_out_payment import (
    CheckOutPaymentUpdateSerializer,
    CheckOutPaymentDeleteSerializer,
)
from pms_apps.checkin_checkout.serializers.requests.create_check_out_key import CheckOutKeyCreateSerializer
from pms_apps.checkin_checkout.serializers.requests.update_check_out_key import (
    CheckOutKeyUpdateSerializer,
    CheckOutKeyDeleteSerializer,
)
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
    CheckOutDocumentsUpdateSerializer,
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
        description="Get all Check-Outs - filter by status, building, assigned employee, "
                     "manager approval, key return status, payment status, request source, search, and date range",
        parameters=[
            OpenApiParameter(name='values', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='page_num', required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='limit', required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='sort_by', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='sort_order', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='search_key', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='status', description='Comma separated: Pending,Inspection Pending,Approved,Active,Completed,Cancelled',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='building', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='assigned_employee_id', description='Comma separated employee IDs',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='manager_approval', description='Comma separated: Pending,Approved,Rejected',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='key_return_status', description='Comma separated: Pending,Returned,Not Returned,Lost',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='payment_status', description='Comma separated: Pending,Paid,Partially Paid,Refunded',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='request_from', description='Comma separated: Tenant,Admin',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='from_date', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='to_date', required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ],
        responses=SwaggerPage.response(description=CheckOutView().data_get, response=CheckOutResponseGetAllSerializer)
    )
    @api_view(["GET"])
    @SerializerValidations(serializer=CheckOutGetAllSerializer).validate
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

    @extend_schema(
        description="Update Check-Out Documents Notes",
        request=CheckOutDocumentsUpdateSerializer,
        responses=SwaggerPage.response(description=CheckOutView().data_update)
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutDocumentsUpdateSerializer).validate
    def update_documents(request: Request) -> Response:
        return CheckOutView().update_documents_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-Out (soft delete)",
        parameters=CheckOutDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=CheckOutView().data_delete)
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckOutDeleteSerializer).validate
    def delete(request: Request) -> Response:
        return CheckOutView().delete_extract(params=request.params)

    @extend_schema(
        description="Upload a document for a Check-Out",
        request=CheckOutDocumentUploadSerializer,
        responses=SwaggerPage.response(description="Document uploaded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckOutDocumentUploadSerializer).validate
    def upload_document(request: Request) -> Response:
        return CheckOutView().upload_document_extract(params=request.params)

    @extend_schema(
        description="Update a Check-Out Document (name, linked_to_label, expiry_date)",
        request=CheckOutDocumentUpdateSerializer,
        responses=SwaggerPage.response(description="Document updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutDocumentUpdateSerializer).validate
    def update_document(request: Request) -> Response:
        return CheckOutView().update_document_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-Out Document",
        parameters=CheckOutDocumentDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Document deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckOutDocumentDeleteSerializer).validate
    def delete_document(request: Request) -> Response:
        return CheckOutView().delete_document_extract(params=request.params)

    @extend_schema(
        description="Create a Check-Out Inspection Item",
        request=CheckOutInspectionItemCreateSerializer,
        responses=SwaggerPage.response(description="Inspection item recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckOutInspectionItemCreateSerializer).validate
    def create_inspection_item(request: Request) -> Response:
        return CheckOutView().create_inspection_item_extract(params=request.params)

    @extend_schema(
        description="Update a Check-Out Inspection Item",
        request=CheckOutInspectionItemUpdateSerializer,
        responses=SwaggerPage.response(description="Inspection item updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutInspectionItemUpdateSerializer).validate
    def update_inspection_item(request: Request) -> Response:
        return CheckOutView().update_inspection_item_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-Out Inspection Item",
        parameters=CheckOutInspectionItemDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Inspection item deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckOutInspectionItemDeleteSerializer).validate
    def delete_inspection_item(request: Request) -> Response:
        return CheckOutView().delete_inspection_item_extract(params=request.params)

    @extend_schema(
        description="Create a Check-Out Utility Reading",
        request=CheckOutUtilityReadingCreateSerializer,
        responses=SwaggerPage.response(description="Utility reading recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckOutUtilityReadingCreateSerializer).validate
    def create_utility_reading(request: Request) -> Response:
        return CheckOutView().create_utility_reading_extract(params=request.params)

    @extend_schema(
        description="Update a Check-Out Utility Reading",
        request=CheckOutUtilityReadingUpdateSerializer,
        responses=SwaggerPage.response(description="Utility reading updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutUtilityReadingUpdateSerializer).validate
    def update_utility_reading(request: Request) -> Response:
        return CheckOutView().update_utility_reading_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-Out Utility Reading",
        parameters=CheckOutUtilityReadingDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Utility reading deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckOutUtilityReadingDeleteSerializer).validate
    def delete_utility_reading(request: Request) -> Response:
        return CheckOutView().delete_utility_reading_extract(params=request.params)

    @extend_schema(
        description="Create a Check-Out Payment",
        request=CheckOutPaymentCreateSerializer,
        responses=SwaggerPage.response(description="Payment recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckOutPaymentCreateSerializer).validate
    def create_payment(request: Request) -> Response:
        return CheckOutView().create_payment_extract(params=request.params)

    @extend_schema(
        description="Update a Check-Out Payment",
        request=CheckOutPaymentUpdateSerializer,
        responses=SwaggerPage.response(description="Payment updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutPaymentUpdateSerializer).validate
    def update_payment(request: Request) -> Response:
        return CheckOutView().update_payment_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-Out Payment",
        parameters=CheckOutPaymentDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Payment deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckOutPaymentDeleteSerializer).validate
    def delete_payment(request: Request) -> Response:
        return CheckOutView().delete_payment_extract(params=request.params)

    @extend_schema(
        description="Create a Check-Out Key",
        request=CheckOutKeyCreateSerializer,
        responses=SwaggerPage.response(description="Key recorded successfully")
    )
    @api_view(["POST"])
    @SerializerValidations(serializer=CheckOutKeyCreateSerializer).validate
    def create_key(request: Request) -> Response:
        return CheckOutView().create_key_extract(params=request.params)

    @extend_schema(
        description="Update a Check-Out Key",
        request=CheckOutKeyUpdateSerializer,
        responses=SwaggerPage.response(description="Key updated successfully")
    )
    @api_view(["PATCH"])
    @SerializerValidations(serializer=CheckOutKeyUpdateSerializer).validate
    def update_key(request: Request) -> Response:
        return CheckOutView().update_key_extract(params=request.params)

    @extend_schema(
        description="Delete a Check-Out Key",
        parameters=CheckOutKeyDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Key deleted successfully")
    )
    @api_view(["DELETE"])
    @SerializerValidations(serializer=CheckOutKeyDeleteSerializer).validate
    def delete_key(request: Request) -> Response:
        return CheckOutView().delete_key_extract(params=request.params)
