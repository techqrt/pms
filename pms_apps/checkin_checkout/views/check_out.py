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
from pms_apps.checkin_checkout.dataclasses.requests.delete_check_out import CheckOutDeleteRequest
from pms_apps.checkin_checkout.dataclasses.requests.upload_check_out_document import CheckOutDocumentUploadRequest
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_inspection_item import CheckOutInspectionItemCreateRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_inspection_item import (
    CheckOutInspectionItemUpdateRequest,
    CheckOutInspectionItemDeleteRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_utility_reading import CheckOutUtilityReadingCreateRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_utility_reading import (
    CheckOutUtilityReadingUpdateRequest,
    CheckOutUtilityReadingDeleteRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_payment import CheckOutPaymentCreateRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_payment import (
    CheckOutPaymentUpdateRequest,
    CheckOutPaymentDeleteRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out_key import CheckOutKeyCreateRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out_key import (
    CheckOutKeyUpdateRequest,
    CheckOutKeyDeleteRequest,
)
from pms_apps.checkin_checkout.models.check_out import CheckOut
from pms_apps.checkin_checkout.models.check_out_document import CheckOutDocument
from pms_apps.checkin_checkout.models.check_out_inspection_item import CheckOutInspectionItem
from pms_apps.checkin_checkout.models.check_out_utility_reading import CheckOutUtilityReading
from pms_apps.checkin_checkout.models.check_out_payment import CheckOutPayment
from pms_apps.checkin_checkout.models.check_out_key import CheckOutKey

from pms_apps.property.image_utils import ImageUtils
from pms_apps.property.models.property import Property
from pms_apps.property.models.property_details import PropertyDetail
from pms_apps.property.models.property_assignment import PropertyAssignment
from pms_apps.property.views import PropertyView
from pms_apps.lead.models.lead import Lead


class CheckOutView:
    def __init__(self):
        self.data_create = "Check-Out recorded successfully"
        self.data_update = "Check-Out updated successfully"
        self.data_get = "Check-Out fetched successfully"
        self.data_delete = "Check-Out deleted successfully"
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
                request_from=params.request_from,
                monthly_rent=params.monthly_rent,
                security_deposit=params.security_deposit,
                advance_rent_received=params.advance_rent_received,
                first_month_rent_paid=params.first_month_rent_paid,
                payment_mode=params.payment_mode,
                maintenance_charges=params.maintenance_charges,
                inspection_required=params.inspection_required,
                inspection_date=params.inspection_date,
                technician_type=params.technician_type,
                inspection_duration=params.inspection_duration,
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

    _OVERVIEW_INFO_FIELDS = {
        'Flat': ['flat_number', 'floor_number', 'building_block', 'flat_configuration',
                 'no_of_bathrooms', 'kitchen_type', 'facing', 'balcony', 'parking',
                 'allowed_tenant_types', 'store_room'],
        'Commercial': ['commercial_category', 'floor_number', 'frontage_width_ft', 'ceiling_height_ft',
                       'no_of_cabins', 'no_of_washrooms', 'loading_area', 'parking_availability',
                       'lease_type', 'lease_tenure_years', 'lock_in_period_months',
                       'allowed_business', 'prohibited_business'],
        'Villa': ['villa_name', 'villa_type', 'villa_configuration', 'project_name',
                  'plot_area_sqft', 'number_of_bedrooms', 'number_of_bathrooms',
                  'living_rooms_count', 'servant_room', 'balcony_or_sitout',
                  'private_parking', 'allowed_tenant_types', 'store_room'],
    }
    _OVERVIEW_FEATURE_FIELDS = {
        'Flat': ['lift', 'security', 'gas_pipeline', 'water_supply', 'intercom',
                 'fire_safety', 'power_backup', 'cctv'],
        'Commercial': ['has_dg_backup', 'lift_type', 'fire_safety_compliant', 'emergency_exit',
                       'gst_applicable', 'gst_percentage'],
        'Villa': ['private_garden', 'terrace_access', 'boundary_wall', 'driveway',
                  'water_supply_24x7', 'security_guard', 'clubhouse_access', 'gym',
                  'childrens_play_area', 'internal_roads', 'street_lights', 'gated_community',
                  'bachelor_allowed', 'pets_allowed', 'power_backup', 'cctv'],
    }
    _OVERVIEW_CHARGE_FIELDS = {
        'Flat': ['maintenance_charge_amount', 'electricity_charge_amount', 'water_charge_amount'],
        'Commercial': ['commercial_maintenance_charge_type', 'maintenance_charge_amount',
                       'electricity_charge_amount', 'water_charge_amount', 'security_deposit_months'],
        'Villa': ['villa_maintenance_charge_type', 'gardening_charges', 'maintenance_charge_amount',
                  'electricity_charge_amount', 'water_charge_amount'],
    }
    _PROPERTY_DETAILS_VARIANT_FIELDS = {
        'Flat': {'configuration': 'flat_configuration', 'bathrooms': 'no_of_bathrooms',
                 'facing': 'facing', 'plotAreaSqft': None, 'projectOrSociety': None, 'nameOrNumber': 'flat_number'},
        'Commercial': {'configuration': None, 'bathrooms': 'no_of_washrooms',
                       'facing': None, 'plotAreaSqft': None, 'projectOrSociety': None, 'nameOrNumber': 'commercial_category'},
        'Villa': {'configuration': 'villa_configuration', 'bathrooms': 'number_of_bathrooms',
                  'facing': 'facing', 'plotAreaSqft': 'plot_area_sqft', 'projectOrSociety': 'project_name', 'nameOrNumber': 'villa_name'},
    }
    _REQUIRED_DOCUMENT_TYPES = ["Tenant ID Proof", "Address Proof", "Inspection Photo", "Agreement Copy"]
    _EXPIRY_SOON_THRESHOLD_DAYS = 30

    def _fetch_property_context(self, property_id: int) -> dict:
        from django.forms.models import model_to_dict
        property_data = Property.get(property_id=property_id) or {}
        detail_obj = PropertyDetail.get_by_property(property_id=property_id)
        rental_type = property_data.get('rental_type')
        detail_dict = model_to_dict(detail_obj) if detail_obj else {}
        property_view = PropertyView()
        property_dict = {}
        property_view._categorize_property_details(property_dict, detail_dict, rental_type)
        landlord_details = None
        if detail_obj and detail_obj.landlord_id:
            landlord_row = Lead.objects.filter(lead_id=detail_obj.landlord_id).values(
                'lead_id', 'first_name', 'last_name', 'address',
                'lead_id__phone_number', 'lead_id__email'
            ).first()
            if landlord_row:
                landlord_details = {
                    "landlordId": landlord_row.get('lead_id'),
                    "name": f"{landlord_row.get('first_name') or ''} {landlord_row.get('last_name') or ''}".strip(),
                    "mobileNumber": landlord_row.get('lead_id__phone_number'),
                    "email": landlord_row.get('lead_id__email'),
                    "address": landlord_row.get('address'),
                }
        from pms_apps.property.models.property_photos import PropertyPhotos
        photos_urls = []
        for photo in PropertyPhotos.objects.filter(property_id=property_id):
            if photo.photo:
                if str(photo.photo).startswith('http://') or str(photo.photo).startswith('https://'):
                    photos_urls.append(str(photo.photo))
                else:
                    photos_urls.append(ImageUtils.get_photo_url(str(photo.photo)))
        return {
            "property_data": property_data, "detail_obj": detail_obj, "detail_dict": detail_dict,
            "rental_type": rental_type, "property_dict": property_dict,
            "property_view": property_view, "landlord_details": landlord_details, "photos_urls": photos_urls,
        }

    def _build_overview(self, data: dict, check_out_id: int) -> dict:
        items = list(CheckOutInspectionItem.get_all_for_check_out(check_out_id))
        issue_items = [i for i in items if i['inspection_status'] == 'Issue']
        payments = list(CheckOutPayment.get_all_for_check_out(check_out_id))
        readings = list(CheckOutUtilityReading.get_all_for_check_out(check_out_id))
        keys = list(CheckOutKey.get_all_for_check_out(check_out_id))

        total_utility_charges = sum((r['charges'] or 0) for r in readings)
        total_deductions = sum((p['amount'] or 0) for p in payments)
        security_deposit = data.get('securityDeposit') or 0
        try:
            from decimal import Decimal
            sd = Decimal(str(security_deposit))
            td = Decimal(str(total_deductions))
            refundable = sd - td
        except Exception:
            refundable = 0

        inspection_status = "Completed" if data.get('managerApproval') == 'Approved' else (
            "In Progress" if data.get('inspectionRequired') == 'Yes' else "Pending"
        )

        keys_returned = sum(1 for k in keys if k['status'] == 'Returned')
        keys_pending = sum(1 for k in keys if k['status'] == 'Pending')

        pipeline_stages = [
            {"stage": "Request Raised", "status": "completed" if data.get('checkOutStatus') else "pending"},
            {"stage": "Inspection", "status": "completed" if data.get('managerApproval') == 'Approved' else "pending"},
            {"stage": "Repair & Damage", "status": "completed" if all(i['repair_status'] == 'Repaired' for i in issue_items) and issue_items else "pending"},
            {"stage": "Utility Reading", "status": "completed" if readings else "pending"},
            {"stage": "Settlement", "status": "completed" if data.get('paymentStatus') in ('Paid', 'Refunded') else "pending"},
            {"stage": "Key Return", "status": "completed" if data.get('keyReturnStatus') == 'Returned' else "pending"},
            {"stage": "Completed", "status": "completed" if data.get('checkOutStatus') == 'Completed' else "pending"},
        ]
        completed_stages = sum(1 for s in pipeline_stages if s['status'] == 'completed')
        overall_progress = int((completed_stages / len(pipeline_stages)) * 100)

        activity_timeline = []
        if data.get('createdAt'):
            activity_timeline.append({"event": "Check-Out Requested", "description": f"Check-Out request was raised by {data.get('tenantName')}", "timestamp": data.get('createdAt')})
        if data.get('inspectionDate'):
            activity_timeline.append({"event": "Inspection Completed", "description": f"Inspection has been completed by {(data.get('assignedEmployee') or {}).get('name')}", "timestamp": data.get('inspectionDate')})
        if readings:
            activity_timeline.append({"event": "Utility Readings Captured", "description": "Utility Readings were recorded", "timestamp": data.get('updatedAt')})
        if issue_items:
            activity_timeline.append({"event": "Repair & Damage Added", "description": f"{len(issue_items)} repair & damage items added", "timestamp": data.get('updatedAt')})

        return {
            "summaryCards": {
                "inspectionStatus": inspection_status,
                "repairDamageItems": len(issue_items),
                "utilityCharges": total_utility_charges,
                "outstanding": float(refundable) if refundable else 0,
            },
            "progressPipeline": pipeline_stages,
            "overallProgress": overall_progress,
            "activityTimeline": list(reversed(activity_timeline)),
            "inspectionSummary": {
                "inspectionDate": data.get('inspectionDate'),
                "inspector": (data.get('assignedEmployee') or {}).get('name'),
                "status": inspection_status,
                "overallCondition": "Good" if not issue_items else "Issues",
                "inspectorComments": data.get('supervisorRemarks'),
            },
            "financialSummary": {
                "outstandingRent": data.get('monthlyRent'),
                "utilityCharges": total_utility_charges,
                "damageCharges": sum((i.get('cost') or 0) for i in issue_items),
                "otherCharges": data.get('rentAdjustmentAmount'),
                "totalDeductions": total_deductions,
                "securityDeposit": security_deposit,
                "refundableAmount": float(refundable) if refundable else 0,
            },
        }

    def _build_tenant_details(self, data: dict, check_out_id: int, context: dict) -> dict:
        payments = list(CheckOutPayment.get_all_for_check_out(check_out_id))
        total_paid = sum((p['amount'] or 0) for p in payments if p['status'] == 'Paid')
        total_pending = sum((p['amount'] or 0) for p in payments if p['status'] == 'Pending')
        readings = list(CheckOutUtilityReading.get_all_for_check_out(check_out_id))
        utility_charges = sum((r['charges'] or 0) for r in readings)

        detail_dict = context.get('detail_dict', {})
        photos_urls = context.get('photos_urls', [])
        common = context.get('property_dict', {}).get('propertyDetails', {})

        tenant_docs = list(CheckOutDocument.objects.filter(
            check_out_id=check_out_id,
            document_type__in=["Tenant ID Proof", "Passport Copy"],
            is_active=True
        ))

        return {
            "personalDetails": {
                "tenantCode": data.get('tenantCode'), "tenantName": data.get('tenantName'),
                "tenantType": data.get('tenantType'), "dateOfBirth": data.get('dateOfBirth'),
                "gender": data.get('gender'), "maritalStatus": data.get('maritalStatus'),
                "tenantNationality": data.get('tenantNationality'),
            },
            "contactDetails": {
                "tenantMobileNumber": data.get('tenantMobileNumber'),
                "tenantEmail": data.get('tenantEmail'),
                "tenantAddress": data.get('tenantAddress'),
                "emergencyContactName": data.get('emergencyContactName'),
                "emergencyContactNumber": data.get('emergencyContactNumber'),
            },
            "identificationDetails": {
                "tenantCivilId": data.get('tenantCivilId'),
                "tenantPassportNumber": data.get('tenantPassportNumber'),
            },
            "professionalDetails": {
                "profession": data.get('profession'), "companyName": data.get('companyName'),
            },
            "currentAddress": {
                "propertyName": data.get('buildingName'),
                "address": common.get('addressLine1'),
                "unitType": detail_dict.get('flat_configuration') or detail_dict.get('villa_configuration'),
                "areaSqft": detail_dict.get('carpet_area_sqft'),
                "floor": detail_dict.get('floor_number'),
                "photos": photos_urls[:1],
            },
            "agreementInformation": {
                "agreementStartDate": data.get('agreementStartDate') if 'agreementStartDate' in data else None,
                "agreementEndDate": data.get('agreementEndDate') if 'agreementEndDate' in data else None,
                "rentAmount": data.get('monthlyRent'),
                "securityDeposit": data.get('securityDeposit'),
                "advanceRent": data.get('advanceRentReceived'),
                "maintenanceCharges": data.get('maintenanceCharges'),
                "paymentMode": data.get('paymentMode'),
            },
            "outstandingSummary": {
                "totalPaid": total_paid,
                "totalPending": total_pending,
                "utilityCharges": utility_charges,
                "totalDeductions": total_paid + total_pending,
            },
            "tenantDocuments": [
                {
                    "documentId": d.check_out_document_id,
                    "documentType": d.document_type,
                    "documentName": d.document_name or (str(d.file).rsplit('/', 1)[-1] if d.file else None),
                    "file": self._resolve_file_url(str(d.file) if d.file else None),
                    "uploadedOn": d.created_at,
                }
                for d in tenant_docs
            ],
        }

    @staticmethod
    def _compute_duration_label(start_date, end_date):
        if not start_date or not end_date:
            return None
        from datetime import date as date_cls
        if isinstance(start_date, str):
            start_date = date_cls.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date_cls.fromisoformat(end_date)
        months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        if end_date.day < start_date.day:
            months -= 1
        return f"{max(months, 0)} Months"

    def _build_property_details(self, data: dict, context: dict) -> dict:
        detail_dict = context["detail_dict"]
        rental_type = context["rental_type"]
        property_dict = context["property_dict"]
        landlord_details = context["landlord_details"]
        photos_urls = context["photos_urls"]
        common = property_dict.get('propertyDetails', {})
        variant_fields = self._PROPERTY_DETAILS_VARIANT_FIELDS.get(rental_type, {})

        def variant(key):
            field = variant_fields.get(key)
            return detail_dict.get(field) if field else None

        assignment = None
        property_assignment_id = data.get('propertyAssignmentId')
        if property_assignment_id:
            assignment = PropertyAssignment.objects.filter(
                property_assignment_id=property_assignment_id
            ).first()
        if assignment:
            duration = (
                f"{assignment.agreement_duration_months} Months"
                if assignment.agreement_duration_months
                else self._compute_duration_label(assignment.rental_start_date, assignment.rental_end_date)
            )
            rental_details = {
                "rentStartDate": assignment.rental_start_date,
                "rentEndDate": assignment.rental_end_date,
                "agreementDuration": duration,
                "maintenanceRequired": assignment.maintenance_required,
                "maintenanceStatus": assignment.maintenance_status,
                "paymentMode": assignment.payment_mode,
            }
            agreement_details = {
                "agreementType": assignment.agreement_type,
                "agreementPreparedBy": assignment.agreement_prepared_by.name if assignment.agreement_prepared_by_id else None,
                "agreementStatus": assignment.agreement_status,
            }
        else:
            rental_details = {}
            agreement_details = {}

        project_or_society = variant('projectOrSociety') or common.get('buildingName')
        name_or_number = variant('nameOrNumber')
        property_name = " ".join(str(p) for p in [project_or_society, name_or_number] if p) or common.get('propertyCode')
        address = ", ".join(filter(None, [common.get('addressLine1'), common.get('addressLine2'), common.get('city'), common.get('country')]))
        created_by_name = (data.get('createdBy') or {}).get('name')
        return {
            "propertyName": property_name, "address": address,
            "monthlyRent": common.get('monthlyRent'), "photos": photos_urls,
            "basicInformation": {
                "propertyType": rental_type, "propertyCode": common.get('propertyCode'),
                "projectOrSociety": project_or_society, "nameOrNumber": name_or_number,
                "totalFloors": common.get('totalFloors'), "yearBuilt": common.get('yearOfConstruction'),
            },
            "configurationAndArea": {
                "configuration": variant('configuration'), "carpetAreaSqft": common.get('carpetAreaSqft'),
                "builtupAreaSqft": common.get('builtupAreaSqft'), "plotAreaSqft": variant('plotAreaSqft'),
                "bathrooms": variant('bathrooms'), "facing": variant('facing'),
            },
            "rentalAndFinancialDetails": {
                "monthlyRent": common.get('monthlyRent'), "securityDeposit": common.get('securityDepositAmount'),
                "maintenance": detail_dict.get('maintenance_charge_amount'),
                "electricity": common.get('electricityChargeType'), "waterCharges": common.get('waterChargeType'),
            },
            "ownership": {"landlordName": landlord_details.get('name') if landlord_details else None},
            "rentalDetails": rental_details,
            "agreementDetails": agreement_details,
            "amenitiesAndFacilities": [
                f.replace('_', ' ').title()
                for f in self._OVERVIEW_FEATURE_FIELDS.get(rental_type, [])
                if detail_dict.get(f) is True
            ],
            "residentialAddress": {
                "address": address, "city": common.get('city'), "state": common.get('state'),
                "poBox": common.get('pincode'), "googleMap": common.get('googleMapLocation'),
            },
            "systemInformation": {
                "createdBy": created_by_name, "createdOn": data.get('createdAt'), "lastUpdated": data.get('updatedAt'),
            },
        }

    def _build_inspection(self, data: dict, check_out_id: int) -> dict:
        items = list(CheckOutInspectionItem.get_all_for_check_out(check_out_id))
        total = len(items)
        good = sum(1 for i in items if i['inspection_status'] == 'Good')
        issues = sum(1 for i in items if i['inspection_status'] == 'Issue')
        na = sum(1 for i in items if i['inspection_status'] == 'Not Applicable')
        category_breakdown = {}
        for item in items:
            cat = item['category']
            b = category_breakdown.setdefault(cat, {"category": cat, "totalItems": 0, "good": 0, "issues": 0, "notApplicable": 0})
            b["totalItems"] += 1
            if item['inspection_status'] == 'Good':
                b["good"] += 1
            elif item['inspection_status'] == 'Issue':
                b["issues"] += 1
            elif item['inspection_status'] == 'Not Applicable':
                b["notApplicable"] += 1
        inspections_list = []
        for b in category_breakdown.values():
            b["status"] = "Issues" if b["issues"] > 0 else "Good"
            inspections_list.append(b)
        top_issues = sorted(
            [{"category": b["category"], "issueCount": b["issues"]} for b in category_breakdown.values() if b["issues"] > 0],
            key=lambda e: e["issueCount"], reverse=True,
        )
        recent_issues = [
            {
                "checkOutInspectionItemId": i['check_out_inspection_item_id'],
                "itemName": i['item_name'], "category": i['category'], "severity": i['severity'],
                "photo": self._resolve_file_url(str(i['photo']) if i['photo'] else None),
            }
            for i in items if i['inspection_status'] == 'Issue'
        ]
        photos_urls = [
            self._resolve_file_url(str(d.file) if d.file else None)
            for d in CheckOutDocument.objects.filter(check_out_id=check_out_id, document_type="Inspection Photo", is_active=True)
        ]
        return {
            "summary": {"totalItems": total, "checked": good + issues, "good": good, "issuesFound": issues, "notApplicable": na},
            "inspectionsList": inspections_list,
            "inspectionOverview": {
                "inspectionDate": data.get('inspectionDate'),
                "inspector": (data.get('assignedEmployee') or {}).get('name'),
                "inspectionDuration": data.get('inspectionDuration'),
                "overallStatus": "Issues" if issues > 0 else "Good",
                "nextInspectionDue": data.get('nextInspectionDue'),
            },
            "inspectionNotes": data.get('supervisorRemarks'),
            "topIssuesCategories": top_issues,
            "inspectionPhotos": photos_urls,
            "recentIssues": recent_issues,
        }

    def _build_repair_damage(self, data: dict, check_out_id: int) -> dict:
        items = list(CheckOutInspectionItem.get_all_for_check_out(check_out_id))
        issue_items = [i for i in items if i['inspection_status'] == 'Issue']
        pending_count = sum(1 for i in issue_items if i['repair_status'] in ('Required', 'Pending'))
        repaired_count = sum(1 for i in issue_items if i['repair_status'] == 'Repaired')
        approved_count = sum(1 for i in issue_items if i['item_approval_status'] == 'Approved')
        na_count = sum(1 for i in issue_items if i['repair_status'] is None)
        estimated_cost = sum((i.get('cost') or 0) for i in issue_items)
        property_label = ", ".join(filter(None, [data.get('flatUnitNumber'), data.get('buildingName')]))
        return {
            "summary": {
                "totalItems": len(issue_items),
                "repairItems": pending_count,
                "repairedItems": repaired_count,
                "noActionRequired": na_count,
                "estimatedCost": estimated_cost,
                "approved": approved_count,
            },
            "issueList": [
                {
                    "issueId": i['check_out_inspection_item_id'], "category": i['category'],
                    "issueDescription": i['item_name'], "status": i['repair_status'],
                    "assignedTo": i['assigned_to__name'], "targetDate": i['target_date'],
                    "cost": i.get('cost'),
                }
                for i in issue_items
            ],
            "approvalSummary": {
                "recommendedBy": (data.get('recommendedBy') or {}).get('name'),
                "approvedBy": (data.get('approvedBy') or {}).get('name'),
                "approvedOn": data.get('approvedOn'),
                "overallStatus": data.get('gmApproval'),
                "landlordConsent": data.get('landlordConsent'),
                "financeAlertGenerated": data.get('financeAlertGenerated'),
                "quotationAmount": data.get('quotationAmount'),
                "rentAdjustmentAmount": data.get('rentAdjustmentAmount'),
            },
            "pendingRepairs": [
                {
                    "checkOutInspectionItemId": i['check_out_inspection_item_id'],
                    "itemName": i['item_name'], "property": property_label,
                    "severity": i['severity'], "cost": i.get('cost'),
                }
                for i in issue_items if i['repair_status'] in ('Required', 'Pending')
            ],
            "repairedPhotos": [
                self._resolve_file_url(str(i['photo']) if i['photo'] else None)
                for i in issue_items if i['repair_status'] == 'Repaired' and i['photo']
            ],
            "recentResolvedIssues": [
                {
                    "checkOutInspectionItemId": i['check_out_inspection_item_id'],
                    "itemName": i['item_name'], "category": i['category'], "status": "Done",
                }
                for i in issue_items if i['repair_status'] == 'Repaired'
            ],
            "documents": [
                {
                    "documentId": d.check_out_document_id,
                    "documentType": d.document_type,
                    "documentName": d.document_name or (str(d.file).rsplit('/', 1)[-1] if d.file else None),
                    "file": self._resolve_file_url(str(d.file) if d.file else None),
                    "uploadedOn": d.created_at,
                }
                for d in CheckOutDocument.objects.filter(
                    check_out_id=check_out_id, document_type="Repair Document", is_active=True
                )
            ],
        }

    def _build_utility_readings(self, data: dict, check_out_id: int) -> dict:
        from decimal import Decimal
        readings = list(CheckOutUtilityReading.get_all_for_check_out(check_out_id))
        total_charges = sum((r['charges'] or 0) for r in readings)
        adjustment_raw = data.get('utilityAdjustmentAmount')
        adjustment = Decimal(str(adjustment_raw)) if adjustment_raw is not None else Decimal('0')
        not_applicable_count = sum(1 for r in readings if r['status'] == 'Not Applicable')
        total_payable = total_charges - adjustment
        total_balance = total_charges

        # Try to fetch check-in readings for comparison
        check_in_readings_map = {}
        check_in_id = data.get('checkInId')
        if check_in_id:
            from pms_apps.checkin_checkout.models.check_in_utility_reading import CheckInUtilityReading
            ci_readings = CheckInUtilityReading.objects.filter(check_in_id=check_in_id, is_active=True).values(
                'utility_type', 'reading_value'
            )
            check_in_readings_map = {r['utility_type']: r['reading_value'] for r in ci_readings}

        readings_list = [
            {
                "checkOutUtilityReadingId": r['check_out_utility_reading_id'],
                "utility": r['utility_type'], "meterNo": r['meter_no'],
                "checkInReading": check_in_readings_map.get(r['utility_type']),
                "checkOutReading": r['reading_value'], "consumption": r['consumption'],
                "unit": r['unit'], "ratePerUnit": r['rate_per_unit'],
                "charges": r['charges'], "status": r['status'],
            }
            for r in readings
        ]
        reading_overview = sorted(
            [{"utility": r['utility_type'], "charges": r['charges'] or 0} for r in readings],
            key=lambda e: e["charges"], reverse=True,
        )
        meter_photos = [
            self._resolve_file_url(str(d.file) if d.file else None)
            for d in CheckOutDocument.objects.filter(check_out_id=check_out_id, document_type="Meter Reading Photo", is_active=True)
        ]
        return {
            "summary": {
                "totalBalance": total_balance,
                "totalPayable": total_payable,
                "totalUtilities": len(readings),
                "totalCurrentCharge": total_charges,
                "adjustment": adjustment,
                "notApplicable": not_applicable_count,
            },
            "readingsList": readings_list,
            "utilitiesOverview": {
                "totalBalance": total_balance,
                "totalPayable": total_payable,
                "totalUtilities": len(readings),
                "totalUnits": len(readings),
                "totalCurrentCharge": total_charges,
                "notApplicable": not_applicable_count,
            },
            "readingOverview": reading_overview,
            "meterPhotos": meter_photos,
        }

    def _build_finance_details(self, data: dict, check_out_id: int) -> dict:
        from decimal import Decimal
        payments = list(CheckOutPayment.get_all_for_check_out(check_out_id))
        total_charges = sum((p['amount'] or 0) for p in payments)
        total_tax = sum((p.get('tax') or 0) for p in payments)
        total_with_tax = total_charges + total_tax
        total_paid = sum((p['amount'] or 0) for p in payments if p['status'] == 'Paid')
        pending_settlements = sum((p['amount'] or 0) for p in payments if p['status'] == 'Pending')

        security_deposit = data.get('securityDeposit') or 0
        try:
            sd = Decimal(str(security_deposit))
            td = Decimal(str(total_charges))
            refund_amount = sd - td
        except Exception:
            refund_amount = 0

        return {
            "summaryCards": {
                "totalCharges": total_charges,
                "totalPayments": total_paid,
                "pendingSettlements": pending_settlements,
                "refundAmount": float(refund_amount) if refund_amount else 0,
            },
            "chargesAndDeductions": [
                {
                    "checkOutPaymentId": p['check_out_payment_id'],
                    "chargeType": data.get('chargeType'),
                    "description": p['description'],
                    "amount": p['amount'],
                    "tax": p.get('tax'),
                    "total": float((p['amount'] or 0) + (p.get('tax') or 0)),
                    "status": p['status'],
                    "paymentDate": p['payment_date'],
                    "receiptRefNo": p['receipt_ref_no'],
                }
                for p in payments
            ],
            "settlementSummary": {
                "securityDeposit": security_deposit,
                "totalDeductions": total_charges,
                "totalPaid": total_paid,
                "refundAmount": float(refund_amount) if refund_amount else 0,
                "settlementStatus": data.get('paymentStatus'),
            },
            "financeOverview": {
                "chargeType": data.get('chargeType'),
                "totalAmount": data.get('totalAmount'),
                "paymentStatus": data.get('paymentStatus'),
                "paymentDate": data.get('paymentDate'),
                "transactionId": data.get('transactionId'),
                "paymentProof": data.get('paymentProof'),
            },
        }

    def _build_key_return(self, data: dict, check_out_id: int) -> dict:
        keys = list(CheckOutKey.get_all_for_check_out(check_out_id))
        total_keys = len(keys)
        returned_keys = sum(1 for k in keys if k['status'] == 'Returned')
        pending_keys = sum(1 for k in keys if k['status'] == 'Pending')
        lost_keys = 0  # tracked via key_return_status on CheckOut

        assigned_employee_name = (data.get('assignedEmployee') or {}).get('name')
        payments = list(CheckOutPayment.get_all_for_check_out(check_out_id))
        finance_status = None
        if payments:
            finance_status = "Completed" if all(p['status'] == 'Paid' for p in payments) else "Pending"

        timeline_events = [
            {"event": "Key Return Expected", "timestamp": data.get('expectedReturnDate'), "actor": data.get('tenantName')},
            {"event": "Key Returned", "timestamp": data.get('keyReturnDate'), "actor": data.get('tenantName')},
        ]
        key_return_timeline = [e for e in timeline_events if e['timestamp']]

        key_photos = [
            self._resolve_file_url(str(d.file) if d.file else None)
            for d in CheckOutDocument.objects.filter(check_out_id=check_out_id, document_type="Key Return Photo", is_active=True)
        ]

        return {
            "summaryCards": {
                "totalKeysIssued": total_keys,
                "totalKeysReturned": returned_keys,
                "pendingKeys": pending_keys,
                "lostUnreturnedKeys": lost_keys,
            },
            "keyReturnInformation": {
                "keyReturnStatus": data.get('keyReturnStatus'),
                "keyNumber": data.get('keyNumber'),
                "keyReturn": data.get('keyReturn'),
                "expectedReturnDate": data.get('expectedReturnDate'),
                "keyReturnDate": data.get('keyReturnDate'),
                "totalKeys": total_keys,
                "tenantName": data.get('tenantName'),
                "tenantContact": data.get('tenantMobileNumber'),
                "confirmationReceived": data.get('confirmationReceived'),
                "receivedBy": assigned_employee_name,
            },
            "keyReturnTimeline": key_return_timeline,
            "keyDetails": [
                {
                    "checkOutKeyId": k['check_out_key_id'],
                    "keyNumber": k['key_number'], "keyType": k['key_type'], "status": k['status'],
                }
                for k in keys
            ],
            "keyReturnPhotos": key_photos,
            "keyReturnSummary": {
                "tenantName": data.get('tenantName'),
                "unitNo": data.get('flatUnitNumber'),
                "checkOutDate": data.get('checkOutDate'),
                "totalKeyIssued": total_keys,
                "keysReturned": returned_keys,
                "keysPending": pending_keys,
                "status": data.get('keyReturnStatus'),
            },
            "relatedInformation": {
                "checkOutCode": data.get('checkOutCode'),
                "checkInId": data.get('checkInId'),
                "property": ", ".join(filter(None, [data.get('flatUnitNumber'), data.get('buildingName')])),
                "tenant": data.get('tenantName'),
                "financeStatus": finance_status,
                "checkOutStatus": data.get('checkOutStatus'),
            },
        }

    def _build_documents(self, data: dict, check_out_id: int) -> dict:
        from datetime import date as date_cls
        documents = list(CheckOutDocument.objects.filter(check_out_id=check_out_id, is_active=True))
        all_documents = [
            {
                "documentId": d.check_out_document_id,
                "documentName": str(d.file).rsplit('/', 1)[-1] if d.file else None,
                "documentType": d.document_type,
                "category": CheckOutDocument.CATEGORY_BY_TYPE.get(d.document_type, "Other"),
                "linkedTo": d.linked_to_label,
                "uploadedBy": d.uploaded_by.name if d.uploaded_by_id else None,
                "uploadedOn": d.created_at,
                "file": self._resolve_file_url(str(d.file) if d.file else None),
            }
            for d in documents
        ]
        today = date_cls.today()
        expiring_soon = []
        uploaded_types = set()
        for d in documents:
            uploaded_types.add(d.document_type)
            if not d.expiry_date:
                continue
            days_remaining = (d.expiry_date - today).days
            if 0 <= days_remaining <= self._EXPIRY_SOON_THRESHOLD_DAYS:
                expiring_soon.append({
                    "documentId": d.check_out_document_id, "documentType": d.document_type,
                    "linkedTo": d.linked_to_label, "expiryDate": d.expiry_date,
                    "daysRemaining": days_remaining,
                })
        expiring_soon.sort(key=lambda e: e["daysRemaining"])
        missing_documents = [
            {"documentType": dt, "tenant": data.get('tenantName')}
            for dt in self._REQUIRED_DOCUMENT_TYPES if dt not in uploaded_types
        ]

        category_summary = {}
        for d in documents:
            cat = CheckOutDocument.CATEGORY_BY_TYPE.get(d.document_type, "Other")
            category_summary[cat] = category_summary.get(cat, 0) + 1

        recent_uploads = sorted(all_documents, key=lambda d: d['uploadedOn'] or '', reverse=True)[:5]

        return {
            "summary": {
                "totalDocuments": len(documents) + len(missing_documents),
                "uploadedDocuments": len(documents),
                "expiringSoon": len(expiring_soon),
                "missingDocuments": len(missing_documents),
            },
            "allDocuments": all_documents,
            "expiringSoon": expiring_soon,
            "missingDocuments": missing_documents,
            "documentsSummary": category_summary,
            "recentUploads": recent_uploads,
            "notes": data.get('tenantRemarks'),
        }

    @Common(response_handler=CheckOutResponseGetSerializer).exception_handler
    def get_extract(self, params: CheckOutGetRequest):
        detail = CheckOut.get(params.check_out_id)
        if not detail:
            raise ValueError(self.data_no_match)

        data = json.loads(CheckOutUtils().mapper(data=[detail]))[0]
        data['paymentProof'] = self._resolve_file_url(data.get('paymentProof'))

        data['documents'] = [
            {
                "documentId": d.check_out_document_id,
                "documentType": d.document_type,
                "file": self._resolve_file_url(str(d.file) if d.file else None),
            }
            for d in CheckOutDocument.objects.filter(check_out_id=params.check_out_id, is_active=True)
        ]

        property_context = self._fetch_property_context(data.get('propertyId'))
        data['overview'] = self._build_overview(data, params.check_out_id)
        data['tenantDetails'] = self._build_tenant_details(data, params.check_out_id, property_context)
        data['propertyDetails'] = self._build_property_details(data, property_context)
        data['inspection'] = self._build_inspection(data, params.check_out_id)
        data['repairDamage'] = self._build_repair_damage(data, params.check_out_id)
        data['utilityReadings'] = self._build_utility_readings(data, params.check_out_id)
        data['financeDetails'] = self._build_finance_details(data, params.check_out_id)
        data['keyReturn'] = self._build_key_return(data, params.check_out_id)
        data['documentsTab'] = self._build_documents(data, params.check_out_id)

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
            request_from=params.request_from,
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
            tenant_address=params.tenant_address,
            date_of_birth=params.date_of_birth,
            gender=params.gender,
            marital_status=params.marital_status,
            emergency_contact_name=params.emergency_contact_name,
            emergency_contact_number=params.emergency_contact_number,
            profession=params.profession,
            company_name=params.company_name,
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
            property_assignment_id=params.property_assignment_id,
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
            inspection_duration=params.inspection_duration,
            manager_approval=params.manager_approval,
            inspection_priority=params.inspection_priority,
            issue_identified=params.issue_identified,
            supervisor_remarks=params.supervisor_remarks,
            next_inspection_due=params.next_inspection_due,
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
            repair_priority=params.repair_priority,
            recommended_by_id=params.recommended_by_id,
            approved_by_id=params.approved_by_id,
            approved_on=params.approved_on,
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
            settlement_status=params.settlement_status,
            finance_description=params.finance_description,
            payment_proof_processed=processed,
            updated_by=params.user_id,
        )
        return self._update_response(check_out_id)

    @Common().exception_handler
    def update_key_return_extract(self, params: CheckOutKeyReturnUpdateRequest):
        check_out_id = CheckOut.update_key_return(
            check_out_id=params.check_out_id,
            key_number=params.key_number,
            key_type=params.key_type,
            key_available=params.key_available,
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

    @Common().exception_handler
    def delete_extract(self, params: CheckOutDeleteRequest):
        if not CheckOut.get(params.check_out_id):
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            CheckOut.delete(check_out_id=params.check_out_id)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )

    @Common().exception_handler
    def upload_document_extract(self, params: CheckOutDocumentUploadRequest):
        if not CheckOut.get(params.check_out_id):
            raise ValueError(self.data_no_match)

        processed = ImageUtils.process_photo(
            params.file, upload_path="checkin_checkout/check_out_documents/"
        )
        if processed is None:
            raise ValueError("Invalid file data")

        if params.document_type in CheckOutDocument.IMAGE_ONLY_DOCUMENT_TYPES:
            file_name = processed[1] if isinstance(processed, tuple) else processed.name
            extension = file_name.rsplit('.', 1)[-1] if '.' in file_name else ''
            if not ImageUtils.is_image_extension(extension):
                raise ValueError(f"{params.document_type} must be an image file (jpg, png, gif, webp)")

        doc = CheckOutDocument()
        doc.check_out_id = params.check_out_id
        doc.document_type = params.document_type
        doc.document_name = params.document_name
        doc.linked_to_label = params.linked_to_label
        doc.expiry_date = params.expiry_date
        doc.uploaded_by_id = params.user_id

        if isinstance(processed, tuple) and processed[0] == 'url':
            doc.file = processed[1]
            doc.save()
        else:
            doc.save()
            doc.file.save(processed.name, processed, save=True)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Document uploaded successfully",
                data={"check_out_document_id": doc.check_out_document_id}
            )
        )

    @Common().exception_handler
    def create_inspection_item_extract(self, params: CheckOutInspectionItemCreateRequest):
        if not CheckOut.get(params.check_out_id):
            raise ValueError(self.data_no_match)

        item = CheckOutInspectionItem()
        if params.photo:
            processed = ImageUtils.process_photo(
                params.photo, upload_path="checkin_checkout/check_out_inspection_items/"
            )
            if isinstance(processed, tuple) and processed[0] == 'url':
                item.photo = processed[1]
            elif processed:
                item.photo.save(processed.name, processed, save=False)

        item_id = item.create(
            check_out_id=params.check_out_id,
            category=params.category,
            item_name=params.item_name,
            inspection_status=params.inspection_status,
            severity=params.severity,
            repair_status=params.repair_status,
            item_approval_status=params.item_approval_status,
            assigned_to_id=params.assigned_to_id,
            target_date=params.target_date,
            cost=params.cost,
            remarks=params.remarks,
            created_by=params.user_id,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Inspection item recorded successfully",
                data={"check_out_inspection_item_id": item_id}
            )
        )

    @Common().exception_handler
    def update_inspection_item_extract(self, params: CheckOutInspectionItemUpdateRequest):
        item_id = CheckOutInspectionItem.update(
            check_out_inspection_item_id=params.check_out_inspection_item_id,
            category=params.category,
            item_name=params.item_name,
            inspection_status=params.inspection_status,
            severity=params.severity,
            repair_status=params.repair_status,
            item_approval_status=params.item_approval_status,
            assigned_to_id=params.assigned_to_id,
            target_date=params.target_date,
            cost=params.cost,
            remarks=params.remarks,
            updated_by=params.user_id,
        )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Inspection item updated successfully",
                data={"check_out_inspection_item_id": item_id}
            )
        )

    @Common().exception_handler
    def delete_inspection_item_extract(self, params: CheckOutInspectionItemDeleteRequest):
        CheckOutInspectionItem.delete(params.check_out_inspection_item_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Inspection item deleted successfully", data={})
        )

    @Common().exception_handler
    def create_utility_reading_extract(self, params: CheckOutUtilityReadingCreateRequest):
        if not CheckOut.get(params.check_out_id):
            raise ValueError(self.data_no_match)

        reading = CheckOutUtilityReading()
        reading_id = reading.create(
            check_out_id=params.check_out_id,
            utility_type=params.utility_type,
            meter_no=params.meter_no,
            reading_value=params.reading_value,
            consumption=params.consumption,
            unit=params.unit,
            rate_per_unit=params.rate_per_unit,
            charges=params.charges,
            status=params.status,
            remarks=params.remarks,
            created_by=params.user_id,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Utility reading recorded successfully",
                data={"check_out_utility_reading_id": reading_id}
            )
        )

    @Common().exception_handler
    def update_utility_reading_extract(self, params: CheckOutUtilityReadingUpdateRequest):
        reading_id = CheckOutUtilityReading.update(
            check_out_utility_reading_id=params.check_out_utility_reading_id,
            utility_type=params.utility_type,
            meter_no=params.meter_no,
            reading_value=params.reading_value,
            consumption=params.consumption,
            unit=params.unit,
            rate_per_unit=params.rate_per_unit,
            charges=params.charges,
            status=params.status,
            remarks=params.remarks,
            updated_by=params.user_id,
        )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Utility reading updated successfully",
                data={"check_out_utility_reading_id": reading_id}
            )
        )

    @Common().exception_handler
    def delete_utility_reading_extract(self, params: CheckOutUtilityReadingDeleteRequest):
        CheckOutUtilityReading.delete(params.check_out_utility_reading_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Utility reading deleted successfully", data={})
        )

    @Common().exception_handler
    def create_payment_extract(self, params: CheckOutPaymentCreateRequest):
        if not CheckOut.get(params.check_out_id):
            raise ValueError(self.data_no_match)

        payment = CheckOutPayment()
        payment_id = payment.create(
            check_out_id=params.check_out_id,
            description=params.description,
            amount=params.amount,
            tax=params.tax,
            status=params.status,
            payment_date=params.payment_date,
            receipt_ref_no=params.receipt_ref_no,
            remarks=params.remarks,
            created_by=params.user_id,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Payment recorded successfully",
                data={"check_out_payment_id": payment_id}
            )
        )

    @Common().exception_handler
    def update_payment_extract(self, params: CheckOutPaymentUpdateRequest):
        payment_id = CheckOutPayment.update(
            check_out_payment_id=params.check_out_payment_id,
            description=params.description,
            amount=params.amount,
            tax=params.tax,
            status=params.status,
            payment_date=params.payment_date,
            receipt_ref_no=params.receipt_ref_no,
            remarks=params.remarks,
            updated_by=params.user_id,
        )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Payment updated successfully",
                data={"check_out_payment_id": payment_id}
            )
        )

    @Common().exception_handler
    def delete_payment_extract(self, params: CheckOutPaymentDeleteRequest):
        CheckOutPayment.delete(params.check_out_payment_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Payment deleted successfully", data={})
        )

    @Common().exception_handler
    def create_key_extract(self, params: CheckOutKeyCreateRequest):
        if not CheckOut.get(params.check_out_id):
            raise ValueError(self.data_no_match)

        key = CheckOutKey()
        key_id = key.create(
            check_out_id=params.check_out_id,
            key_number=params.key_number,
            key_type=params.key_type,
            status=params.status,
            remarks=params.remarks,
            created_by=params.user_id,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Key recorded successfully",
                data={"check_out_key_id": key_id}
            )
        )

    @Common().exception_handler
    def update_key_extract(self, params: CheckOutKeyUpdateRequest):
        key_id = CheckOutKey.update(
            check_out_key_id=params.check_out_key_id,
            key_number=params.key_number,
            key_type=params.key_type,
            status=params.status,
            remarks=params.remarks,
            updated_by=params.user_id,
        )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Key updated successfully",
                data={"check_out_key_id": key_id}
            )
        )

    @Common().exception_handler
    def delete_key_extract(self, params: CheckOutKeyDeleteRequest):
        CheckOutKey.delete(params.check_out_key_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Key deleted successfully", data={})
        )
