import json

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from pms_apps.common.common import Common
from pms_apps.common.dataclasses.get_all import GetAll
from pms_apps.common.utils import Utils

from pms_apps.checkin_checkout.utils import CheckOutUtils
from pms_apps.checkin_checkout.serializers.response.get_check_out import CheckOutResponseGetSerializer
from pms_apps.checkin_checkout.serializers.response.get_all_check_out import CheckOutResponseGetAllSerializer

from pms_apps.checkin_checkout.dataclasses.requests.create_check_out import CheckOutCreateRequest
from pms_apps.checkin_checkout.dataclasses.requests.get_check_out import CheckOutGetRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out import (
    CheckOutInformationUpdateRequest,
    CheckOutTenantDetailsUpdateRequest,
    CheckOutPropertyDetailsUpdateRequest,
    CheckOutRentalDetailsUpdateRequest,
    CheckOutPropertyInspectionUpdateRequest,
    CheckOutRepairDamageUpdateRequest,
    CheckOutUtilityMeterReadingsUpdateRequest,
    CheckOutFinanceDetailsUpdateRequest,
    CheckOutKeyReturnUpdateRequest,
    CheckOutCommentsUpdateRequest,
)
from pms_apps.checkin_checkout.models.check_out import CheckOut
from pms_apps.checkin_checkout.models.check_out_document import CheckOutDocument

from pms_apps.property.image_utils import ImageUtils
from pms_apps.property.models.property import Property
from pms_apps.property.models.property_assignment import PropertyAssignment
from pms_apps.lead.models.lead import Lead


class CheckOutView:
    def __init__(self):
        self.data_create = "Check-Out recorded successfully"
        self.data_update = "Check-Out updated successfully"
        self.data_get = "Check-Out fetched successfully"
        self.data_no_match = "No matching check-out found"

    @staticmethod
    def _resolve_file_url(file_value: str):
        if not file_value:
            return None
        if file_value.startswith('http://') or file_value.startswith('https://'):
            return file_value
        return ImageUtils.get_photo_url(file_value)

    @Common().exception_handler
    def create_extract(self, params: CheckOutCreateRequest):
        if not Property.objects.filter(property_id=params.property_id).exists():
            raise ValueError(f"Invalid Property ID: {params.property_id}")

        if params.property_assignment_id and not PropertyAssignment.objects.filter(
            property_assignment_id=params.property_assignment_id
        ).exists():
            raise ValueError(f"Invalid Property Assignment ID: {params.property_assignment_id}")

        if params.tenant_id and not Lead.objects.filter(lead_id=params.tenant_id).exists():
            raise ValueError(f"Invalid Tenant ID: {params.tenant_id}")

        payment_proof = params.payment_proof

        with transaction.atomic():
            check_out = CheckOut()
            check_out_id = check_out.create(
                property_id=params.property_id,
                created_by=params.user_id,
                property_assignment_id=params.property_assignment_id,
                check_in_id=params.check_in_id,
                tenant_id=params.tenant_id,
                assigned_employee_id=params.assigned_employee_id,
                check_out_date=params.check_out_date,
                check_out_status=params.check_out_status,
                remarks_notes=params.remarks_notes,
                monthly_rent=params.monthly_rent,
                security_deposit=params.security_deposit,
                advance_rent_received=params.advance_rent_received,
                first_month_rent_paid=params.first_month_rent_paid,
                payment_mode=params.payment_mode,
                maintenance_charges=params.maintenance_charges,
                inspection_required=params.inspection_required,
                inspection_date=params.inspection_date,
                technician_type=params.technician_type,
                manager_approval=params.manager_approval,
                issue_identified=params.issue_identified or "",
                supervisor_remarks=params.supervisor_remarks or "",
                repair_required=params.repair_required,
                quotation_amount=params.quotation_amount,
                inventory_available=params.inventory_available,
                gm_approval=params.gm_approval,
                landlord_consent=params.landlord_consent,
                finance_alert_generated=params.finance_alert_generated,
                rent_adjustment_amount=params.rent_adjustment_amount,
                electricity_meter_reading=params.electricity_meter_reading,
                water_meter_reading=params.water_meter_reading,
                gas_meter_reading=params.gas_meter_reading,
                charge_type=params.charge_type,
                total_amount=params.total_amount,
                payment_status=params.payment_status,
                payment_date=params.payment_date,
                transaction_id=params.transaction_id,
                key_number=params.key_number,
                key_return=params.key_return,
                expected_return_date=params.expected_return_date,
                confirmation_received=params.confirmation_received,
                key_return_date=params.key_return_date,
                key_return_status=params.key_return_status,
                internal_comments=params.internal_comments,
                tenant_remarks=params.tenant_remarks,
                special_instructions=params.special_instructions,
            )

            if payment_proof:
                processed = ImageUtils.process_photo(
                    payment_proof, upload_path="checkin_checkout/payment_proofs/"
                )
                if isinstance(processed, tuple) and processed[0] == 'url':
                    check_out.payment_proof = processed[1]
                elif processed:
                    check_out.payment_proof.save(processed.name, processed, save=False)
                check_out.save()

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_create,
                data={"check_out_id": check_out_id, "check_out_code": check_out.check_out_code}
            )
        )

    @Common(response_handler=CheckOutResponseGetSerializer).exception_handler
    def get_extract(self, params: CheckOutGetRequest):
        detail = CheckOut.get(params.check_out_id)
        if not detail:
            raise ValueError(self.data_no_match)

        data = json.loads(CheckOutUtils().mapper(data=[detail]))[0]
        data['paymentProof'] = self._resolve_file_url(data.get('paymentProof'))

        data['documents'] = [
            {
                "documentId": document.check_out_document_id,
                "documentType": document.document_type,
                "file": self._resolve_file_url(str(document.file) if document.file else None),
            }
            for document in CheckOutDocument.objects.filter(check_out_id=params.check_out_id, is_active=True)
        ]

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common(response_handler=CheckOutResponseGetAllSerializer).exception_handler
    def get_all_extract(self, params: GetAll):
        reversed_mapped = CheckOutUtils.reverse_mapper([params.sort_by, params.filter_key])

        check_out_list = CheckOut.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            filter_key=reversed_mapped.get(params.filter_key),
            filter_value=params.filter_value,
            search_key=params.search_key,
            from_date=params.from_date,
            to_date=params.to_date,
        )

        pages = Paginator(check_out_list, per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        columns = [column for column in params.values.split(',') if column]

        check_out_utils = CheckOutUtils(columns_required=columns)
        data = json.loads(check_out_utils.mapper(data=page_data))

        data = Utils.add_page_parameter(
            final_data=data,
            page_num=params.page_num,
            total_page=pages.num_pages,
            present_url=params.present_url,
            next_page_required=True if pages.num_pages != params.page_num else False
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    def _update_response(self, check_out_id: int) -> Response:
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_update,
                data={"check_out_id": check_out_id}
            )
        )

    @Common().exception_handler
    def update_information_extract(self, params: CheckOutInformationUpdateRequest):
        check_out_id = CheckOut.update_information(
            check_out_id=params.check_out_id,
            assigned_employee_id=params.assigned_employee_id,
            check_out_date=params.check_out_date,
            check_out_status=params.check_out_status,
            remarks_notes=params.remarks_notes,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_tenant_details_extract(self, params: CheckOutTenantDetailsUpdateRequest):
        check_out_id = CheckOut.update_tenant_details(
            check_out_id=params.check_out_id,
            tenant_code=params.tenant_code,
            tenant_name=params.tenant_name,
            tenant_type=params.tenant_type,
            tenant_mobile_number=params.tenant_mobile_number,
            tenant_email=params.tenant_email,
            tenant_civil_id=params.tenant_civil_id,
            tenant_passport_number=params.tenant_passport_number,
            tenant_nationality=params.tenant_nationality,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_property_details_extract(self, params: CheckOutPropertyDetailsUpdateRequest):
        check_out_id = CheckOut.update_property_details(
            check_out_id=params.check_out_id,
            property_type=params.property_type,
            property_code=params.property_code,
            building_name=params.building_name,
            flat_unit_number=params.flat_unit_number,
            floor_number=params.floor_number,
            property_status=params.property_status,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_rental_details_extract(self, params: CheckOutRentalDetailsUpdateRequest):
        check_out_id = CheckOut.update_rental_details(
            check_out_id=params.check_out_id,
            monthly_rent=params.monthly_rent,
            security_deposit=params.security_deposit,
            advance_rent_received=params.advance_rent_received,
            first_month_rent_paid=params.first_month_rent_paid,
            payment_mode=params.payment_mode,
            maintenance_charges=params.maintenance_charges,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_property_inspection_extract(self, params: CheckOutPropertyInspectionUpdateRequest):
        check_out_id = CheckOut.update_property_inspection(
            check_out_id=params.check_out_id,
            inspection_required=params.inspection_required,
            inspection_date=params.inspection_date,
            technician_type=params.technician_type,
            manager_approval=params.manager_approval,
            issue_identified=params.issue_identified,
            supervisor_remarks=params.supervisor_remarks,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_repair_damage_extract(self, params: CheckOutRepairDamageUpdateRequest):
        check_out_id = CheckOut.update_repair_damage(
            check_out_id=params.check_out_id,
            repair_required=params.repair_required,
            quotation_amount=params.quotation_amount,
            inventory_available=params.inventory_available,
            gm_approval=params.gm_approval,
            landlord_consent=params.landlord_consent,
            finance_alert_generated=params.finance_alert_generated,
            rent_adjustment_amount=params.rent_adjustment_amount,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_utility_meter_readings_extract(self, params: CheckOutUtilityMeterReadingsUpdateRequest):
        check_out_id = CheckOut.update_utility_meter_readings(
            check_out_id=params.check_out_id,
            electricity_meter_reading=params.electricity_meter_reading,
            water_meter_reading=params.water_meter_reading,
            gas_meter_reading=params.gas_meter_reading,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_finance_details_extract(self, params: CheckOutFinanceDetailsUpdateRequest):
        processed = None
        if params.payment_proof:
            processed = ImageUtils.process_photo(
                params.payment_proof, upload_path="checkin_checkout/payment_proofs/"
            )
            if processed is None:
                raise ValueError("Invalid file data")

        check_out_id = CheckOut.update_finance_details(
            check_out_id=params.check_out_id,
            charge_type=params.charge_type,
            total_amount=params.total_amount,
            payment_status=params.payment_status,
            payment_date=params.payment_date,
            transaction_id=params.transaction_id,
            payment_proof_processed=processed,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_key_return_extract(self, params: CheckOutKeyReturnUpdateRequest):
        check_out_id = CheckOut.update_key_return(
            check_out_id=params.check_out_id,
            key_number=params.key_number,
            key_return=params.key_return,
            expected_return_date=params.expected_return_date,
            confirmation_received=params.confirmation_received,
            key_return_date=params.key_return_date,
            key_return_status=params.key_return_status,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_comments_extract(self, params: CheckOutCommentsUpdateRequest):
        check_out_id = CheckOut.update_comments(
            check_out_id=params.check_out_id,
            internal_comments=params.internal_comments,
            tenant_remarks=params.tenant_remarks,
            special_instructions=params.special_instructions,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)
