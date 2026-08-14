import json

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils

from pms_apps.checkin_checkout.utils import CheckInUtils
from pms_apps.checkin_checkout.serializers.response.get import CheckInResponseGetSerializer
from pms_apps.checkin_checkout.serializers.response.get_all import CheckInResponseGetAllSerializer

from pms_apps.checkin_checkout.dataclasses.requests.create_check_in import CheckInCreateRequest
from pms_apps.checkin_checkout.dataclasses.requests.get_all_check_in import CheckInGetAllRequest
from pms_apps.checkin_checkout.dataclasses.requests.get_check_in import CheckInGetRequest
from pms_apps.checkin_checkout.dataclasses.requests.delete_check_in import CheckInDeleteRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in import (
    CheckInInformationUpdateRequest,
    CheckInTenantDetailsUpdateRequest,
    CheckInPropertyDetailsUpdateRequest,
    CheckInRentalDetailsUpdateRequest,
    CheckInPropertyInspectionUpdateRequest,
    CheckInRepairApprovalUpdateRequest,
    CheckInUtilityMeterReadingsUpdateRequest,
    CheckInAgreementDetailsUpdateRequest,
    CheckInKeyHandoverUpdateRequest,
    CheckInCommentsUpdateRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.upload_check_in_document import CheckInDocumentUploadRequest
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_inspection_item import (
    CheckInInspectionItemCreateRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_inspection_item import (
    CheckInInspectionItemUpdateRequest,
    CheckInInspectionItemDeleteRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_utility_reading import (
    CheckInUtilityReadingCreateRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_utility_reading import (
    CheckInUtilityReadingUpdateRequest,
    CheckInUtilityReadingDeleteRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_payment import (
    CheckInPaymentCreateRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_payment import (
    CheckInPaymentUpdateRequest,
    CheckInPaymentDeleteRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in_key import (
    CheckInKeyCreateRequest,
)
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in_key import (
    CheckInKeyUpdateRequest,
    CheckInKeyDeleteRequest,
)
from pms_apps.checkin_checkout.models.check_in import CheckIn
from pms_apps.checkin_checkout.models.check_in_document import CheckInDocument
from pms_apps.checkin_checkout.models.check_in_inspection_item import CheckInInspectionItem
from pms_apps.checkin_checkout.models.check_in_utility_reading import CheckInUtilityReading
from pms_apps.checkin_checkout.models.check_in_payment import CheckInPayment
from pms_apps.checkin_checkout.models.check_in_key import CheckInKey

from pms_apps.property.image_utils import ImageUtils
from pms_apps.property.models.property import Property
from pms_apps.property.models.property_assignment import PropertyAssignment
from pms_apps.property.models.property_details import PropertyDetail
from pms_apps.property.models.property_photos import PropertyPhotos
from pms_apps.property.views import PropertyView
from pms_apps.lead.models.lead import Lead


class CheckInView:
    def __init__(self):
        self.data_create = "Check-In recorded successfully"
        self.data_update = "Check-In updated successfully"
        self.data_get = "Check-In fetched successfully"
        self.data_delete = "Check-In deleted successfully"
        self.data_no_match = "No matching check-in found"

    @Common().exception_handler
    def create_extract(self, params: CheckInCreateRequest):
        if not Property.objects.filter(property_id=params.property_id).exists():
            raise ValueError(f"Invalid Property ID: {params.property_id}")

        if params.property_assignment_id and not PropertyAssignment.objects.filter(
            property_assignment_id=params.property_assignment_id
        ).exists():
            raise ValueError(f"Invalid Property Assignment ID: {params.property_assignment_id}")

        if params.tenant_id and not Lead.objects.filter(lead_id=params.tenant_id).exists():
            raise ValueError(f"Invalid Tenant ID: {params.tenant_id}")

        agreement_document = params.agreement_document

        with transaction.atomic():
            check_in = CheckIn()
            check_in_id = check_in.create(
                property_id=params.property_id,
                created_by=params.user_id,
                property_assignment_id=params.property_assignment_id,
                tenant_id=params.tenant_id,
                assigned_employee_id=params.assigned_employee_id,
                check_in_date=params.check_in_date,
                check_in_status=params.check_in_status,
                remarks_notes=params.remarks_notes,
                alternate_mobile_number=params.alternate_mobile_number,
                move_in_reason=params.move_in_reason,
                number_of_occupants=params.number_of_occupants,
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
                inspection_priority=params.inspection_priority,
                inspection_type=params.inspection_type,
                inspection_duration=params.inspection_duration,
                next_inspection_due=params.next_inspection_due,
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
                inspector_comments=params.inspector_comments or "",
                electricity_meter_reading=params.electricity_meter_reading,
                water_meter_reading=params.water_meter_reading,
                gas_meter_reading=params.gas_meter_reading,
                utility_adjustment_amount=params.utility_adjustment_amount,
                agreement_type=params.agreement_type,
                agreement_status=params.agreement_status,
                agreement_start_date=params.agreement_start_date,
                agreement_end_date=params.agreement_end_date,
                agreement_template=params.agreement_template,
                agreement_number=params.agreement_number,
                generated_on=params.generated_on,
                generated_by_id=params.generated_by_id,
                submitted_to_tenant_on=params.submitted_to_tenant_on,
                tenant_signed_on=params.tenant_signed_on,
                manager_signed_on=params.manager_signed_on,
                signed_by_id=params.signed_by_id,
                renewal_reminder_date=params.renewal_reminder_date,
                auto_reminder_enabled=params.auto_reminder_enabled,
                agreement_notes=params.agreement_notes or "",
                key_number=params.key_number,
                key_type=params.key_type,
                key_available=params.key_available,
                key_booking_date=params.key_booking_date,
                confirmation_received=params.confirmation_received,
                key_delivery_date=params.key_delivery_date,
                key_handover_status=params.key_handover_status,
                expected_handover_date=params.expected_handover_date,
                handover_notes=params.handover_notes or "",
                tenant_confirmation_notes=params.tenant_confirmation_notes or "",
                key_booked_on=params.key_booked_on,
                key_booked_by_id=params.key_booked_by_id,
                key_prepared_on=params.key_prepared_on,
                key_notified_on=params.key_notified_on,
                handover_completed_on=params.handover_completed_on,
                handed_over_by_id=params.handed_over_by_id,
                internal_comments=params.internal_comments,
                tenant_remarks=params.tenant_remarks,
                special_instructions=params.special_instructions,
                property_created_date=params.property_created_date,
                listed_for_rent_date=params.listed_for_rent_date,
                tenant_assigned_date=params.tenant_assigned_date,
                assigned_to_employee_date=params.assigned_to_employee_date,
                property_occupied_date=params.property_occupied_date,
            )

            if agreement_document:
                processed = ImageUtils.process_photo(
                    agreement_document, upload_path="checkin_checkout/check_in_agreements/"
                )
                if isinstance(processed, tuple) and processed[0] == 'url':
                    check_in.agreement_document = processed[1]
                elif processed:
                    check_in.agreement_document.save(processed.name, processed, save=False)
                check_in.save()

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_create,
                data={"check_in_id": check_in_id, "check_in_code": check_in.check_in_code}
            )
        )

    @staticmethod
    def _resolve_file_url(file_value: str):
        if not file_value:
            return None
        if file_value.startswith('http://') or file_value.startswith('https://'):
            return file_value
        return ImageUtils.get_photo_url(file_value)

    # Type-specific PropertyDetail fields, split by what each Overview widget needs.
    # Source of truth for field names: PropertyView._categorize_property_details.
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

    # Property Details tab: variant-specific field names per logical concept.
    _PROPERTY_DETAILS_VARIANT_FIELDS = {
        'Flat': {
            'configuration': 'flat_configuration',
            'bathrooms': 'no_of_bathrooms',
            'facing': 'facing',
            'plotAreaSqft': None,
            'projectOrSociety': None,
            'nameOrNumber': 'flat_number',
        },
        'Commercial': {
            'configuration': None,
            'bathrooms': 'no_of_washrooms',
            'facing': None,
            'plotAreaSqft': None,
            'projectOrSociety': None,
            'nameOrNumber': 'commercial_category',
        },
        'Villa': {
            'configuration': 'villa_configuration',
            'bathrooms': 'number_of_bathrooms',
            'facing': 'facing',
            'plotAreaSqft': 'plot_area_sqft',
            'projectOrSociety': 'project_name',
            'nameOrNumber': 'villa_name',
        },
    }

    def _fetch_property_context(self, property_id: int) -> dict:
        property_data = Property.get(property_id=property_id) or {}
        detail_obj = PropertyDetail.get_by_property(property_id=property_id)
        rental_type = property_data.get('rental_type')

        from django.forms.models import model_to_dict
        detail_dict = model_to_dict(detail_obj) if detail_obj else {}

        property_dict = {}
        property_view = PropertyView()
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

        photos_urls = []
        for photo in PropertyPhotos.objects.filter(property_id=property_id):
            if photo.photo:
                if str(photo.photo).startswith('http://') or str(photo.photo).startswith('https://'):
                    photos_urls.append(str(photo.photo))
                else:
                    photos_urls.append(ImageUtils.get_photo_url(str(photo.photo)))

        return {
            "property_data": property_data,
            "detail_obj": detail_obj,
            "detail_dict": detail_dict,
            "rental_type": rental_type,
            "property_dict": property_dict,
            "property_view": property_view,
            "landlord_details": landlord_details,
            "photos_urls": photos_urls,
        }

    def _build_overview(self, check_in_data: dict, documents: list, context: dict) -> dict:
        property_data = context["property_data"]
        detail_dict = context["detail_dict"]
        rental_type = context["rental_type"]
        property_dict = context["property_dict"]
        property_view = context["property_view"]
        landlord_details = context["landlord_details"]
        photos_urls = context["photos_urls"]

        to_camel = property_view._to_camel_case
        info_extra = {
            to_camel(field): detail_dict.get(field)
            for field in self._OVERVIEW_INFO_FIELDS.get(rental_type, []) if field in detail_dict
        }
        feature_fields = {
            to_camel(field): detail_dict.get(field)
            for field in self._OVERVIEW_FEATURE_FIELDS.get(rental_type, []) if field in detail_dict
        }
        charge_extra = {
            to_camel(field): detail_dict.get(field)
            for field in self._OVERVIEW_CHARGE_FIELDS.get(rental_type, []) if field in detail_dict
        }

        property_information = {
            "rentalType": rental_type,
            "rentalFor": property_data.get('rental_for'),
            "block": property_data.get('block'),
            "floor": property_data.get('floor'),
            "flatNumber": property_data.get('flat_number'),
            "dimensionAreaSqft": property_data.get('dimension_area_sqft'),
            **property_dict.get('propertyDetails', {}),
            **info_extra,
        }
        # Payment Due Date / Rent Increase Date belong to the Rent & Charges widget, not here.
        property_information.pop('paymentDueDate', None)
        property_information.pop('rentIncreaseDate', None)

        property_features = feature_fields

        rent_and_charges = {
            "monthlyRent": check_in_data.get('monthlyRent'),
            "securityDeposit": check_in_data.get('securityDeposit'),
            "maintenanceFee": check_in_data.get('maintenanceCharges'),
            "lateFeeType": detail_dict.get('late_fee_type'),
            "lateFeeValue": detail_dict.get('late_fee_value'),
            "paymentDueDate": detail_dict.get('payment_due_date'),
            "rentIncreaseDate": detail_dict.get('rent_increase_date'),
            **charge_extra,
        }

        activity_timeline = {
            "propertyCreatedDate": check_in_data.get('propertyCreatedDate'),
            "listedForRentDate": check_in_data.get('listedForRentDate'),
            "tenantAssignedDate": check_in_data.get('tenantAssignedDate'),
            "assignedToEmployeeDate": check_in_data.get('assignedToEmployeeDate'),
            "propertyOccupiedDate": check_in_data.get('propertyOccupiedDate'),
        }

        return {
            "propertyInformation": property_information,
            "rentAndCharges": rent_and_charges,
            "activityTimeline": activity_timeline,
            "landlordDetails": landlord_details,
            "propertyFeatures": property_features,
            "tenantDocuments": documents,
            "photos": photos_urls,
        }

    @staticmethod
    def _build_tenant_details(check_in_data: dict) -> dict:
        personal_details = {
            "tenantCode": check_in_data.get('tenantCode'),
            "tenantName": check_in_data.get('tenantName'),
            "tenantType": check_in_data.get('tenantType'),
            "dateOfBirth": check_in_data.get('dateOfBirth'),
            "gender": check_in_data.get('gender'),
            "maritalStatus": check_in_data.get('maritalStatus'),
            "tenantNationality": check_in_data.get('tenantNationality'),
        }
        contact_details = {
            "tenantMobileNumber": check_in_data.get('tenantMobileNumber'),
            "tenantEmail": check_in_data.get('tenantEmail'),
            "alternateMobileNumber": check_in_data.get('alternateMobileNumber'),
            "emergencyContactName": check_in_data.get('emergencyContactName'),
            "emergencyContactNumber": check_in_data.get('emergencyContactNumber'),
        }
        identification_details = {
            "tenantCivilId": check_in_data.get('tenantCivilId'),
            "tenantPassportNumber": check_in_data.get('tenantPassportNumber'),
            "tenantAddress": check_in_data.get('tenantAddress'),
        }
        professional_details = {
            "profession": check_in_data.get('profession'),
            "companyName": check_in_data.get('companyName'),
        }
        occupancy_details = {
            "moveInReason": check_in_data.get('moveInReason'),
            "numberOfOccupants": check_in_data.get('numberOfOccupants'),
        }

        return {
            "personalDetails": personal_details,
            "contactDetails": contact_details,
            "identificationDetails": identification_details,
            "professionalDetails": professional_details,
            "occupancyDetails": occupancy_details,
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

    def _build_property_details(self, check_in_data: dict, context: dict) -> dict:
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

        project_or_society = variant('projectOrSociety') or common.get('buildingName')
        name_or_number = variant('nameOrNumber')
        property_name = " ".join(
            str(part) for part in [project_or_society, name_or_number] if part
        ) or common.get('propertyCode')

        address = ", ".join(filter(None, [
            common.get('addressLine1'), common.get('addressLine2'),
            common.get('city'), common.get('country'),
        ]))

        created_by_name = (check_in_data.get('createdBy') or {}).get('name')

        return {
            "propertyName": property_name,
            "address": address,
            "monthlyRent": common.get('monthlyRent'),
            "photos": photos_urls,
            "basicInformation": {
                "propertyType": rental_type,
                "propertyCode": common.get('propertyCode'),
                "projectOrSociety": project_or_society,
                "nameOrNumber": name_or_number,
                "totalFloors": common.get('totalFloors'),
                "yearBuilt": common.get('yearOfConstruction'),
            },
            "configurationAndArea": {
                "configuration": variant('configuration'),
                "carpetAreaSqft": common.get('carpetAreaSqft'),
                "builtupAreaSqft": common.get('builtupAreaSqft'),
                "plotAreaSqft": variant('plotAreaSqft'),
                "bathrooms": variant('bathrooms'),
                "facing": variant('facing'),
            },
            "rentalAndFinancialDetails": {
                "monthlyRent": common.get('monthlyRent'),
                "securityDeposit": common.get('securityDepositAmount'),
                "maintenance": detail_dict.get('maintenance_charge_amount'),
                "electricity": common.get('electricityChargeType'),
                "waterCharges": common.get('waterChargeType'),
            },
            "ownership": {
                "landlordName": landlord_details.get('name') if landlord_details else None,
            },
            "amenitiesAndFacilities": [
                field.replace('_', ' ').title()
                for field in self._OVERVIEW_FEATURE_FIELDS.get(rental_type, [])
                if detail_dict.get(field) is True
            ],
            "rentalDetails": {
                "rentStartDate": check_in_data.get('agreementStartDate'),
                "rentEndDate": check_in_data.get('agreementEndDate'),
                "agreementDuration": self._compute_duration_label(
                    check_in_data.get('agreementStartDate'), check_in_data.get('agreementEndDate')
                ),
                "maintenanceRequired": check_in_data.get('repairRequired'),
                "maintenanceStatus": check_in_data.get('managerApproval'),
            },
            "agreementDetails": {
                "agreementType": check_in_data.get('agreementType'),
                "agreementPreparedBy": created_by_name,
                "agreementDocument": check_in_data.get('agreementDocument'),
                "agreementStatus": check_in_data.get('agreementStatus'),
            },
            "residentialAddress": {
                "address": address,
                "city": common.get('city'),
                "state": common.get('state'),
                "poBox": common.get('pincode'),
                "googleMap": common.get('googleMapLocation'),
            },
            "systemInformation": {
                "createdBy": created_by_name,
                "createdOn": check_in_data.get('createdAt'),
                "lastUpdated": check_in_data.get('updatedAt'),
            },
        }

    def _build_inspection(self, check_in_data: dict, check_in_id: int) -> dict:
        items = list(CheckInInspectionItem.get_all_for_check_in(check_in_id))

        total_items = len(items)
        good_count = sum(1 for item in items if item['inspection_status'] == 'Good')
        issue_count = sum(1 for item in items if item['inspection_status'] == 'Issue')
        na_count = sum(1 for item in items if item['inspection_status'] == 'Not Applicable')

        category_breakdown = {}
        for item in items:
            category = item['category']
            bucket = category_breakdown.setdefault(category, {
                "category": category, "totalItems": 0, "good": 0, "issues": 0, "notApplicable": 0,
            })
            bucket["totalItems"] += 1
            if item['inspection_status'] == 'Good':
                bucket["good"] += 1
            elif item['inspection_status'] == 'Issue':
                bucket["issues"] += 1
            elif item['inspection_status'] == 'Not Applicable':
                bucket["notApplicable"] += 1

        inspections_list = []
        for bucket in category_breakdown.values():
            bucket["status"] = "Issues" if bucket["issues"] > 0 else "Good"
            inspections_list.append(bucket)

        top_issues_categories = sorted(
            [{"category": b["category"], "issueCount": b["issues"]} for b in category_breakdown.values() if b["issues"] > 0],
            key=lambda entry: entry["issueCount"],
            reverse=True,
        )

        recent_issues = [
            {
                "checkInInspectionItemId": item['check_in_inspection_item_id'],
                "itemName": item['item_name'],
                "category": item['category'],
                "severity": item['severity'],
                "photo": self._resolve_file_url(str(item['photo']) if item['photo'] else None),
            }
            for item in items if item['inspection_status'] == 'Issue'
        ]

        photos_urls = [
            self._resolve_file_url(str(document.file) if document.file else None)
            for document in CheckInDocument.objects.filter(
                check_in_id=check_in_id, document_type="Inspection Photo", is_active=True
            )
        ]

        return {
            "summary": {
                "totalItems": total_items,
                "checked": good_count + issue_count,
                "good": good_count,
                "issuesFound": issue_count,
                "notApplicable": na_count,
            },
            "inspectionsList": inspections_list,
            "inspectionOverview": {
                "inspectionType": check_in_data.get('inspectionType'),
                "inspectionDate": check_in_data.get('inspectionDate'),
                "inspector": (check_in_data.get('assignedEmployee') or {}).get('name'),
                "inspectionDuration": check_in_data.get('inspectionDuration'),
                "overallStatus": "Issues" if issue_count > 0 else "Good",
                "nextInspectionDue": check_in_data.get('nextInspectionDue'),
                "priority": check_in_data.get('inspectionPriority'),
            },
            "topIssuesCategories": top_issues_categories,
            "inspectionPhotos": photos_urls,
            "recentIssues": recent_issues,
        }

    def _build_repair_approval(self, check_in_data: dict, check_in_id: int) -> dict:
        items = list(CheckInInspectionItem.get_all_for_check_in(check_in_id))
        issues = [item for item in items if item['inspection_status'] == 'Issue']

        pending_repairs_count = sum(1 for item in issues if item['repair_status'] in ('Required', 'Pending'))
        repaired_count = sum(1 for item in issues if item['repair_status'] == 'Repaired')
        approved_count = sum(1 for item in issues if item['item_approval_status'] == 'Approved')

        property_label = ", ".join(filter(None, [
            check_in_data.get('flatUnitNumber'), check_in_data.get('buildingName'),
        ]))

        issue_list = [
            {
                "issueId": item['check_in_inspection_item_id'],
                "category": item['category'],
                "issueDescription": item['item_name'],
                "status": item['repair_status'],
                "assignedTo": item['assigned_to__name'],
                "targetDate": item['target_date'],
            }
            for item in issues
        ]

        recommended_by_name = (check_in_data.get('recommendedBy') or {}).get('name')
        approved_by_name = (check_in_data.get('approvedBy') or {}).get('name')

        pending_repairs = [
            {
                "checkInInspectionItemId": item['check_in_inspection_item_id'],
                "itemName": item['item_name'],
                "property": property_label,
                "severity": item['severity'],
            }
            for item in issues if item['repair_status'] in ('Required', 'Pending')
        ]

        repaired_photos = [
            self._resolve_file_url(str(item['photo']) if item['photo'] else None)
            for item in issues if item['repair_status'] == 'Repaired' and item['photo']
        ]

        recent_resolved_issues = [
            {
                "checkInInspectionItemId": item['check_in_inspection_item_id'],
                "itemName": item['item_name'],
                "category": item['category'],
                "status": "Done",
            }
            for item in issues if item['repair_status'] == 'Repaired'
        ]

        return {
            "summary": {
                "totalIssues": len(issues),
                "pendingRepairs": pending_repairs_count,
                "repaired": repaired_count,
                "approved": approved_count,
            },
            "issueList": issue_list,
            "approvalSummary": {
                "recommendedBy": recommended_by_name,
                "approvedBy": approved_by_name,
                "approvedOn": check_in_data.get('approvedOn'),
                "overallStatus": check_in_data.get('gmApproval'),
                "inspectorComments": check_in_data.get('inspectorComments'),
                "priority": check_in_data.get('repairPriority'),
            },
            "pendingRepairs": pending_repairs,
            "repairedPhotos": repaired_photos,
            "recentResolvedIssues": recent_resolved_issues,
        }

    def _build_utility_readings(self, check_in_data: dict, check_in_id: int) -> dict:
        from decimal import Decimal

        readings = list(CheckInUtilityReading.get_all_for_check_in(check_in_id))

        total_charges = sum((r['charges'] or 0) for r in readings)
        adjustment_raw = check_in_data.get('utilityAdjustmentAmount')
        adjustment = Decimal(str(adjustment_raw)) if adjustment_raw is not None else Decimal('0')
        not_applicable_count = sum(1 for r in readings if r['status'] == 'Not Applicable')

        readings_list = [
            {
                "checkInUtilityReadingId": r['check_in_utility_reading_id'],
                "utility": r['utility_type'],
                "meterNo": r['meter_no'],
                "checkInReading": r['reading_value'],
                "consumption": r['consumption'],
                "unit": r['unit'],
                "ratePerUnit": r['rate_per_unit'],
                "charges": r['charges'],
                "status": r['status'],
            }
            for r in readings
        ]

        reading_overview = sorted(
            [
                {"utility": r['utility_type'], "charges": r['charges'] or 0}
                for r in readings
            ],
            key=lambda entry: entry["charges"],
            reverse=True,
        )

        return {
            "summary": {
                "totalUtilities": len(readings),
                "totalUnits": len(readings),
                "totalCurrentCharge": total_charges,
                "adjustment": adjustment,
                "notApplicable": not_applicable_count,
            },
            "readingsList": readings_list,
            "utilitiesOverview": {
                "totalPayable": total_charges - adjustment,
                "totalUtilities": len(readings),
                "totalUnits": len(readings),
                "totalCurrentCharge": total_charges,
                "notApplicable": not_applicable_count,
            },
            "readingOverview": reading_overview,
        }

    def _build_agreement(self, check_in_data: dict, check_in_id: int) -> dict:
        from datetime import date as date_cls

        start_date = check_in_data.get('agreementStartDate')
        end_date = check_in_data.get('agreementEndDate')
        duration = self._compute_duration_label(start_date, end_date)
        expiry_in = self._compute_duration_label(date_cls.today().isoformat(), end_date) if end_date else None

        generated_by_name = (check_in_data.get('generatedBy') or {}).get('name')
        signed_by_name = (check_in_data.get('signedBy') or {}).get('name')

        agreement_details = {
            "agreementType": check_in_data.get('agreementType'),
            "agreementTemplate": check_in_data.get('agreementTemplate'),
            "agreementNumber": check_in_data.get('agreementNumber'),
            "generatedOn": check_in_data.get('generatedOn'),
            "agreementDocument": check_in_data.get('agreementDocument'),
            "agreementStatus": check_in_data.get('agreementStatus'),
            "submittedToTenantOn": check_in_data.get('submittedToTenantOn'),
            "startDate": start_date,
            "tenantSignedOn": check_in_data.get('tenantSignedOn'),
            "endDate": end_date,
            "managerSignedOn": check_in_data.get('managerSignedOn'),
            "duration": duration,
            "agreementExpiryIn": expiry_in,
            "rentMonthly": check_in_data.get('monthlyRent'),
            "renewalReminderDate": check_in_data.get('renewalReminderDate'),
            "securityDeposit": check_in_data.get('securityDeposit'),
            "autoReminderEnabled": check_in_data.get('autoReminderEnabled'),
            "advanceRent": check_in_data.get('advanceRentReceived'),
            "maintenanceCharges": check_in_data.get('maintenanceCharges'),
        }

        timeline_events = [
            {
                "event": "Agreement Generated",
                "timestamp": check_in_data.get('generatedOn'),
                "actor": generated_by_name,
            },
            {
                "event": "Submitted To Tenant",
                "timestamp": check_in_data.get('submittedToTenantOn'),
                "actor": generated_by_name,
            },
            {
                "event": "Tenant Signed",
                "timestamp": check_in_data.get('tenantSignedOn'),
                "actor": check_in_data.get('tenantName'),
            },
            {
                "event": "Company Signed",
                "timestamp": check_in_data.get('managerSignedOn'),
                "actor": signed_by_name,
            },
        ]
        if check_in_data.get('agreementStatus') in ('Executed', 'Signed'):
            timeline_events.append({
                "event": "Agreement Completed",
                "timestamp": check_in_data.get('managerSignedOn'),
                "actor": "System",
            })
        agreement_timeline = [event for event in timeline_events if event['timestamp']]

        payments = list(CheckInPayment.get_all_for_check_in(check_in_id))
        total_paid = sum((p['amount'] or 0) for p in payments if p['status'] == 'Paid')

        rent_and_payment_summary = {
            "monthlyRent": check_in_data.get('monthlyRent'),
            "securityDeposit": check_in_data.get('securityDeposit'),
            "advanceRent": check_in_data.get('advanceRentReceived'),
            "totalPaid": total_paid,
            "payments": [
                {
                    "checkInPaymentId": p['check_in_payment_id'],
                    "description": p['description'],
                    "amount": p['amount'],
                    "status": p['status'],
                    "paymentDate": p['payment_date'],
                    "receiptRefNo": p['receipt_ref_no'],
                }
                for p in payments
            ],
        }

        agreement_documents = [
            {
                "documentId": document.check_in_document_id,
                "documentType": document.document_type,
                "file": self._resolve_file_url(str(document.file) if document.file else None),
                "uploadedOn": document.created_at,
                "uploadedBy": document.uploaded_by.name if document.uploaded_by_id else None,
            }
            for document in CheckInDocument.objects.filter(
                check_in_id=check_in_id,
                document_type__in=["Agreement Copy", "Tenant ID Proof", "Company Seal"],
                is_active=True,
            )
        ]

        return {
            "agreementDetails": agreement_details,
            "agreementTimeline": agreement_timeline,
            "rentAndPaymentSummary": rent_and_payment_summary,
            "agreementDocuments": agreement_documents,
            "agreementNotes": check_in_data.get('agreementNotes'),
        }

    def _build_key_handover(self, check_in_data: dict, check_in_id: int) -> dict:
        keys = list(CheckInKey.get_all_for_check_in(check_in_id))

        primary_key = next(
            (k for k in keys if k['key_number'] == check_in_data.get('keyNumber')), None
        ) or (keys[0] if keys else None)
        key_type = check_in_data.get('keyType') or (primary_key['key_type'] if primary_key else None)

        assigned_employee_name = (check_in_data.get('assignedEmployee') or {}).get('name')
        key_booked_by_name = (check_in_data.get('keyBookedBy') or {}).get('name')
        handed_over_by_name = (check_in_data.get('handedOverBy') or {}).get('name') or assigned_employee_name

        key_handover_information = {
            "keyHandoverStatus": check_in_data.get('keyHandoverStatus'),
            "keyNumber": check_in_data.get('keyNumber'),
            "keyType": key_type,
            "keyAvailable": check_in_data.get('keyAvailable'),
            "keyBookingDate": check_in_data.get('keyBookingDate'),
            "expectedHandoverDate": check_in_data.get('expectedHandoverDate'),
            "keyHandoverDate": check_in_data.get('keyDeliveryDate'),
            "handoveredBy": handed_over_by_name,
            "receivedByTenant": check_in_data.get('tenantName'),
            "tenantContact": check_in_data.get('tenantMobileNumber'),
            "confirmationReceived": check_in_data.get('confirmationReceived'),
            "handoverNotes": check_in_data.get('handoverNotes'),
        }

        timeline_events = [
            {
                "event": "Key Booked",
                "timestamp": check_in_data.get('keyBookedOn'),
                "actor": key_booked_by_name,
            },
            {
                "event": "Key Prepared",
                "timestamp": check_in_data.get('keyPreparedOn'),
                "actor": assigned_employee_name,
            },
            {
                "event": "Key Notified",
                "timestamp": check_in_data.get('keyNotifiedOn'),
                "actor": assigned_employee_name,
            },
            {
                "event": "Key Handed Over",
                "timestamp": check_in_data.get('keyDeliveryDate'),
                "actor": check_in_data.get('tenantName'),
            },
            {
                "event": "Handover Completed",
                "timestamp": check_in_data.get('handoverCompletedOn'),
                "actor": check_in_data.get('tenantName'),
            },
        ]
        key_handover_timeline = [event for event in timeline_events if event['timestamp']]

        key_details = [
            {
                "checkInKeyId": k['check_in_key_id'],
                "keyNumber": k['key_number'],
                "keyType": k['key_type'],
                "status": k['status'],
            }
            for k in keys
        ]

        attachments = [
            {
                "documentId": document.check_in_document_id,
                "documentType": document.document_type,
                "file": self._resolve_file_url(str(document.file) if document.file else None),
                "uploadedOn": document.created_at,
                "uploadedBy": document.uploaded_by.name if document.uploaded_by_id else None,
            }
            for document in CheckInDocument.objects.filter(
                check_in_id=check_in_id,
                document_type__in=["Key Handover Photo", "Tenant ID Proof", "Key Receipt"],
                is_active=True,
            )
        ]

        payments = list(CheckInPayment.get_all_for_check_in(check_in_id))
        if payments:
            finance_status = "Completed" if all(p['status'] == 'Paid' for p in payments) else "Pending"
        else:
            finance_status = None

        related_information = {
            "checkInCode": check_in_data.get('checkInCode'),
            "property": ", ".join(filter(None, [
                check_in_data.get('flatUnitNumber'), check_in_data.get('buildingName'),
            ])),
            "tenant": check_in_data.get('tenantName'),
            "agreementNumber": check_in_data.get('agreementNumber'),
            "financeStatus": finance_status,
            "checkInStatus": check_in_data.get('checkInStatus'),
        }

        return {
            "keyHandoverInformation": key_handover_information,
            "keyHandoverTimeline": key_handover_timeline,
            "keyDetails": key_details,
            "attachments": attachments,
            "tenantConfirmation": check_in_data.get('tenantConfirmationNotes'),
            "relatedInformation": related_information,
        }

    # Document types every check-in is expected to have on file.
    _REQUIRED_DOCUMENT_TYPES = ["Tenant ID Proof", "Address Proof", "Police Clearance", "Agreement Signed"]
    _EXPIRY_SOON_THRESHOLD_DAYS = 30

    def _build_documents(self, check_in_data: dict, check_in_id: int) -> dict:
        from datetime import date as date_cls

        documents = list(
            CheckInDocument.objects.filter(check_in_id=check_in_id, is_active=True)
        )

        all_documents = [
            {
                "documentId": document.check_in_document_id,
                "documentName": str(document.file).rsplit('/', 1)[-1] if document.file else None,
                "documentType": document.document_type,
                "category": CheckInDocument.CATEGORY_BY_TYPE.get(document.document_type, "Other"),
                "linkedTo": document.linked_to_label,
                "uploadedBy": document.uploaded_by.name if document.uploaded_by_id else None,
                "uploadedOn": document.created_at,
                "file": self._resolve_file_url(str(document.file) if document.file else None),
            }
            for document in documents
        ]

        today = date_cls.today()
        expiring_soon = []
        for document in documents:
            if not document.expiry_date:
                continue
            days_remaining = (document.expiry_date - today).days
            if 0 <= days_remaining <= self._EXPIRY_SOON_THRESHOLD_DAYS:
                expiring_soon.append({
                    "documentId": document.check_in_document_id,
                    "documentType": document.document_type,
                    "linkedTo": document.linked_to_label,
                    "expiryDate": document.expiry_date,
                    "daysRemaining": days_remaining,
                })
        expiring_soon.sort(key=lambda entry: entry["daysRemaining"])

        uploaded_types = {document.document_type for document in documents}
        missing_documents = [
            {
                "documentType": doc_type,
                "tenant": check_in_data.get('tenantName'),
            }
            for doc_type in self._REQUIRED_DOCUMENT_TYPES if doc_type not in uploaded_types
        ]

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
            "notes": check_in_data.get('tenantConfirmationNotes'),
        }

    @Common(response_handler=CheckInResponseGetSerializer).exception_handler
    def get_extract(self, params: CheckInGetRequest):
        detail = CheckIn.get(params.check_in_id)
        if not detail:
            raise ValueError(self.data_no_match)

        data = json.loads(CheckInUtils().mapper(data=[detail]))[0]
        data['agreementDocument'] = self._resolve_file_url(data.get('agreementDocument'))

        data['documents'] = [
            {
                "documentId": document.check_in_document_id,
                "documentType": document.document_type,
                "file": self._resolve_file_url(str(document.file) if document.file else None),
            }
            for document in CheckInDocument.objects.filter(check_in_id=params.check_in_id, is_active=True)
        ]

        property_context = self._fetch_property_context(data.get('propertyId'))
        data['overview'] = self._build_overview(data, data['documents'], property_context)
        data['tenantDetails'] = self._build_tenant_details(data)
        data['propertyDetails'] = self._build_property_details(data, property_context)
        data['inspection'] = self._build_inspection(data, params.check_in_id)
        data['repairApproval'] = self._build_repair_approval(data, params.check_in_id)
        data['utilityReadings'] = self._build_utility_readings(data, params.check_in_id)
        data['agreement'] = self._build_agreement(data, params.check_in_id)
        data['keyHandover'] = self._build_key_handover(data, params.check_in_id)
        data['documentsTab'] = self._build_documents(data, params.check_in_id)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common(response_handler=CheckInResponseGetAllSerializer).exception_handler
    def get_all_extract(self, params: CheckInGetAllRequest):
        reversed_mapped = CheckInUtils.reverse_mapper([params.sort_by])

        check_in_list = CheckIn.get_all(
            sort_by=reversed_mapped.get(params.sort_by),
            sort_order=params.sort_order,
            status=params.status,
            building=params.building,
            assigned_employee_id=params.assigned_employee_id,
            manager_approval=params.manager_approval,
            key_handover_status=params.key_handover_status,
            search_key=params.search_key,
            from_date=params.from_date,
            to_date=params.to_date,
        )

        pages = Paginator(check_in_list, per_page=params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError('Page limit exceed!')

        page_data = pages.page(params.page_num)
        columns = [column for column in params.values.split(',') if column]

        check_in_utils = CheckInUtils(columns_required=columns)
        data = json.loads(check_in_utils.mapper(data=page_data))

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

    @Common().exception_handler
    def delete_extract(self, params: CheckInDeleteRequest):
        if not CheckIn.get(params.check_in_id):
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            CheckIn.delete(check_in_id=params.check_in_id)

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_delete)
        )

    def _update_response(self, check_in_id: int) -> Response:
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_update,
                data={"check_in_id": check_in_id}
            )
        )

    @Common().exception_handler
    def update_information_extract(self, params: CheckInInformationUpdateRequest):
        check_in_id = CheckIn.update_information(
            check_in_id=params.check_in_id,
            assigned_employee_id=params.assigned_employee_id,
            check_in_date=params.check_in_date,
            check_in_status=params.check_in_status,
            remarks_notes=params.remarks_notes,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_tenant_details_extract(self, params: CheckInTenantDetailsUpdateRequest):
        check_in_id = CheckIn.update_tenant_details(
            check_in_id=params.check_in_id,
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
            alternate_mobile_number=params.alternate_mobile_number,
            emergency_contact_name=params.emergency_contact_name,
            emergency_contact_number=params.emergency_contact_number,
            profession=params.profession,
            company_name=params.company_name,
            move_in_reason=params.move_in_reason,
            number_of_occupants=params.number_of_occupants,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_property_details_extract(self, params: CheckInPropertyDetailsUpdateRequest):
        check_in_id = CheckIn.update_property_details(
            check_in_id=params.check_in_id,
            property_type=params.property_type,
            property_code=params.property_code,
            building_name=params.building_name,
            flat_unit_number=params.flat_unit_number,
            floor_number=params.floor_number,
            property_status=params.property_status,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_rental_details_extract(self, params: CheckInRentalDetailsUpdateRequest):
        check_in_id = CheckIn.update_rental_details(
            check_in_id=params.check_in_id,
            monthly_rent=params.monthly_rent,
            security_deposit=params.security_deposit,
            advance_rent_received=params.advance_rent_received,
            first_month_rent_paid=params.first_month_rent_paid,
            payment_mode=params.payment_mode,
            maintenance_charges=params.maintenance_charges,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_property_inspection_extract(self, params: CheckInPropertyInspectionUpdateRequest):
        check_in_id = CheckIn.update_property_inspection(
            check_in_id=params.check_in_id,
            inspection_required=params.inspection_required,
            inspection_date=params.inspection_date,
            technician_type=params.technician_type,
            manager_approval=params.manager_approval,
            issue_identified=params.issue_identified,
            supervisor_remarks=params.supervisor_remarks,
            inspection_priority=params.inspection_priority,
            inspection_type=params.inspection_type,
            inspection_duration=params.inspection_duration,
            next_inspection_due=params.next_inspection_due,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_repair_approval_extract(self, params: CheckInRepairApprovalUpdateRequest):
        check_in_id = CheckIn.update_repair_approval(
            check_in_id=params.check_in_id,
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
            inspector_comments=params.inspector_comments,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_utility_meter_readings_extract(self, params: CheckInUtilityMeterReadingsUpdateRequest):
        check_in_id = CheckIn.update_utility_meter_readings(
            check_in_id=params.check_in_id,
            electricity_meter_reading=params.electricity_meter_reading,
            water_meter_reading=params.water_meter_reading,
            gas_meter_reading=params.gas_meter_reading,
            utility_adjustment_amount=params.utility_adjustment_amount,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_agreement_details_extract(self, params: CheckInAgreementDetailsUpdateRequest):
        processed = None
        if params.agreement_document:
            processed = ImageUtils.process_photo(
                params.agreement_document, upload_path="checkin_checkout/check_in_agreements/"
            )
            if processed is None:
                raise ValueError("Invalid file data")

        check_in_id = CheckIn.update_agreement_details(
            check_in_id=params.check_in_id,
            agreement_type=params.agreement_type,
            agreement_status=params.agreement_status,
            agreement_start_date=params.agreement_start_date,
            agreement_end_date=params.agreement_end_date,
            agreement_document_processed=processed,
            agreement_template=params.agreement_template,
            agreement_number=params.agreement_number,
            generated_on=params.generated_on,
            generated_by_id=params.generated_by_id,
            submitted_to_tenant_on=params.submitted_to_tenant_on,
            tenant_signed_on=params.tenant_signed_on,
            manager_signed_on=params.manager_signed_on,
            signed_by_id=params.signed_by_id,
            renewal_reminder_date=params.renewal_reminder_date,
            auto_reminder_enabled=params.auto_reminder_enabled,
            agreement_notes=params.agreement_notes,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_key_handover_extract(self, params: CheckInKeyHandoverUpdateRequest):
        check_in_id = CheckIn.update_key_handover(
            check_in_id=params.check_in_id,
            key_number=params.key_number,
            key_type=params.key_type,
            key_available=params.key_available,
            key_booking_date=params.key_booking_date,
            confirmation_received=params.confirmation_received,
            key_delivery_date=params.key_delivery_date,
            key_handover_status=params.key_handover_status,
            expected_handover_date=params.expected_handover_date,
            handover_notes=params.handover_notes,
            tenant_confirmation_notes=params.tenant_confirmation_notes,
            key_booked_on=params.key_booked_on,
            key_booked_by_id=params.key_booked_by_id,
            key_prepared_on=params.key_prepared_on,
            key_notified_on=params.key_notified_on,
            handover_completed_on=params.handover_completed_on,
            handed_over_by_id=params.handed_over_by_id,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def update_comments_extract(self, params: CheckInCommentsUpdateRequest):
        check_in_id = CheckIn.update_comments(
            check_in_id=params.check_in_id,
            internal_comments=params.internal_comments,
            tenant_remarks=params.tenant_remarks,
            special_instructions=params.special_instructions,
            updated_by=params.user_id,
        )
        return self._update_response(check_in_id)

    @Common().exception_handler
    def upload_document_extract(self, params: CheckInDocumentUploadRequest):
        if not CheckIn.get(params.check_in_id):
            raise ValueError(self.data_no_match)

        processed = ImageUtils.process_photo(params.file, upload_path="checkin_checkout/check_in_documents/")
        if not processed:
            raise ValueError("Invalid file data")

        document = CheckInDocument()
        document.check_in_id = params.check_in_id
        document.document_type = params.document_type
        document.linked_to_label = params.linked_to_label
        document.expiry_date = params.expiry_date
        if isinstance(processed, tuple) and processed[0] == 'url':
            document.file = processed[1]
        else:
            document.file.save(processed.name, processed, save=False)
        document.uploaded_by_id = params.user_id
        document.save()

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Document uploaded successfully",
                data={"check_in_document_id": document.check_in_document_id}
            )
        )

    @Common().exception_handler
    def create_inspection_item_extract(self, params: CheckInInspectionItemCreateRequest):
        if not CheckIn.get(params.check_in_id):
            raise ValueError(self.data_no_match)

        item = CheckInInspectionItem()
        if params.photo:
            processed = ImageUtils.process_photo(
                params.photo, upload_path="checkin_checkout/check_in_inspection_items/"
            )
            if isinstance(processed, tuple) and processed[0] == 'url':
                item.photo = processed[1]
            elif processed:
                item.photo.save(processed.name, processed, save=False)

        item_id = item.create(
            check_in_id=params.check_in_id,
            category=params.category,
            item_name=params.item_name,
            inspection_status=params.inspection_status,
            severity=params.severity,
            repair_status=params.repair_status,
            item_approval_status=params.item_approval_status,
            assigned_to_id=params.assigned_to_id,
            target_date=params.target_date,
            remarks=params.remarks,
            created_by=params.user_id,
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Inspection item recorded successfully",
                data={"check_in_inspection_item_id": item_id}
            )
        )

    @Common().exception_handler
    def update_inspection_item_extract(self, params: CheckInInspectionItemUpdateRequest):
        item_id = CheckInInspectionItem.update(
            check_in_inspection_item_id=params.check_in_inspection_item_id,
            category=params.category,
            item_name=params.item_name,
            inspection_status=params.inspection_status,
            severity=params.severity,
            repair_status=params.repair_status,
            item_approval_status=params.item_approval_status,
            assigned_to_id=params.assigned_to_id,
            target_date=params.target_date,
            remarks=params.remarks,
            updated_by=params.user_id,
        )
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message="Inspection item updated successfully",
                data={"check_in_inspection_item_id": item_id}
            )
        )

    @Common().exception_handler
    def delete_inspection_item_extract(self, params: CheckInInspectionItemDeleteRequest):
        CheckInInspectionItem.delete(params.check_in_inspection_item_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Inspection item deleted successfully", data={})
        )

    @Common().exception_handler
    def create_utility_reading_extract(self, params: CheckInUtilityReadingCreateRequest):
        if not CheckIn.get(params.check_in_id):
            raise ValueError(self.data_no_match)

        reading = CheckInUtilityReading()
        reading_id = reading.create(
            check_in_id=params.check_in_id,
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
                data={"check_in_utility_reading_id": reading_id}
            )
        )

    @Common().exception_handler
    def update_utility_reading_extract(self, params: CheckInUtilityReadingUpdateRequest):
        reading_id = CheckInUtilityReading.update(
            check_in_utility_reading_id=params.check_in_utility_reading_id,
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
                data={"check_in_utility_reading_id": reading_id}
            )
        )

    @Common().exception_handler
    def delete_utility_reading_extract(self, params: CheckInUtilityReadingDeleteRequest):
        CheckInUtilityReading.delete(params.check_in_utility_reading_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Utility reading deleted successfully", data={})
        )

    @Common().exception_handler
    def create_payment_extract(self, params: CheckInPaymentCreateRequest):
        if not CheckIn.get(params.check_in_id):
            raise ValueError(self.data_no_match)

        payment = CheckInPayment()
        payment_id = payment.create(
            check_in_id=params.check_in_id,
            description=params.description,
            amount=params.amount,
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
                data={"check_in_payment_id": payment_id}
            )
        )

    @Common().exception_handler
    def update_payment_extract(self, params: CheckInPaymentUpdateRequest):
        payment_id = CheckInPayment.update(
            check_in_payment_id=params.check_in_payment_id,
            description=params.description,
            amount=params.amount,
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
                data={"check_in_payment_id": payment_id}
            )
        )

    @Common().exception_handler
    def delete_payment_extract(self, params: CheckInPaymentDeleteRequest):
        CheckInPayment.delete(params.check_in_payment_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Payment deleted successfully", data={})
        )

    @Common().exception_handler
    def create_key_extract(self, params: CheckInKeyCreateRequest):
        if not CheckIn.get(params.check_in_id):
            raise ValueError(self.data_no_match)

        key = CheckInKey()
        key_id = key.create(
            check_in_id=params.check_in_id,
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
                data={"check_in_key_id": key_id}
            )
        )

    @Common().exception_handler
    def update_key_extract(self, params: CheckInKeyUpdateRequest):
        key_id = CheckInKey.update(
            check_in_key_id=params.check_in_key_id,
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
                data={"check_in_key_id": key_id}
            )
        )

    @Common().exception_handler
    def delete_key_extract(self, params: CheckInKeyDeleteRequest):
        CheckInKey.delete(params.check_in_key_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message="Key deleted successfully", data={})
        )
