import pandas
import json

from pms_apps.common.common import Common


class CheckInUtils:
    def __init__(self, columns_required: list = []) -> None:
        self.columns_required = columns_required
        self.mapped_columns_name = {
            'check_in_id': 'checkInId',
            'check_in_code': 'checkInCode',
            'check_in_date': 'checkInDate',
            'check_in_status': 'checkInStatus',
            'remarks_notes': 'remarksNotes',
            'property_id': 'propertyId',
            'property_assignment_id': 'propertyAssignmentId',
            'tenant_id': 'tenantId',
            'assigned_employee_id': 'assignedEmployeeId',
            'assigned_employee__name': 'assignedEmployee.name',
            'tenant_code': 'tenantCode',
            'tenant_name': 'tenantName',
            'tenant_type': 'tenantType',
            'tenant_mobile_number': 'tenantMobileNumber',
            'tenant_email': 'tenantEmail',
            'tenant_civil_id': 'tenantCivilId',
            'tenant_passport_number': 'tenantPassportNumber',
            'tenant_nationality': 'tenantNationality',
            'tenant_address': 'tenantAddress',
            'date_of_birth': 'dateOfBirth',
            'gender': 'gender',
            'marital_status': 'maritalStatus',
            'alternate_mobile_number': 'alternateMobileNumber',
            'emergency_contact_name': 'emergencyContactName',
            'emergency_contact_number': 'emergencyContactNumber',
            'profession': 'profession',
            'company_name': 'companyName',
            'move_in_reason': 'moveInReason',
            'number_of_occupants': 'numberOfOccupants',
            'property_type': 'propertyType',
            'property_code': 'propertyCode',
            'building_name': 'buildingName',
            'flat_unit_number': 'flatUnitNumber',
            'floor_number': 'floorNumber',
            'property_status': 'propertyStatus',
            'monthly_rent': 'monthlyRent',
            'security_deposit': 'securityDeposit',
            'advance_rent_received': 'advanceRentReceived',
            'first_month_rent_paid': 'firstMonthRentPaid',
            'payment_mode': 'paymentMode',
            'maintenance_charges': 'maintenanceCharges',
            'inspection_required': 'inspectionRequired',
            'inspection_date': 'inspectionDate',
            'technician_type': 'technicianType',
            'manager_approval': 'managerApproval',
            'issue_identified': 'issueIdentified',
            'supervisor_remarks': 'supervisorRemarks',
            'inspection_priority': 'inspectionPriority',
            'inspection_type': 'inspectionType',
            'inspection_duration': 'inspectionDuration',
            'next_inspection_due': 'nextInspectionDue',
            'repair_required': 'repairRequired',
            'quotation_amount': 'quotationAmount',
            'inventory_available': 'inventoryAvailable',
            'gm_approval': 'gmApproval',
            'landlord_consent': 'landlordConsent',
            'finance_alert_generated': 'financeAlertGenerated',
            'rent_adjustment_amount': 'rentAdjustmentAmount',
            'repair_priority': 'repairPriority',
            'recommended_by_id': 'recommendedById',
            'recommended_by__name': 'recommendedBy.name',
            'approved_by_id': 'approvedById',
            'approved_by__name': 'approvedBy.name',
            'approved_on': 'approvedOn',
            'inspector_comments': 'inspectorComments',
            'electricity_meter_reading': 'electricityMeterReading',
            'water_meter_reading': 'waterMeterReading',
            'gas_meter_reading': 'gasMeterReading',
            'utility_adjustment_amount': 'utilityAdjustmentAmount',
            'agreement_type': 'agreementType',
            'agreement_status': 'agreementStatus',
            'agreement_start_date': 'agreementStartDate',
            'agreement_end_date': 'agreementEndDate',
            'agreement_document': 'agreementDocument',
            'agreement_template': 'agreementTemplate',
            'agreement_number': 'agreementNumber',
            'generated_on': 'generatedOn',
            'generated_by_id': 'generatedById',
            'generated_by__name': 'generatedBy.name',
            'submitted_to_tenant_on': 'submittedToTenantOn',
            'tenant_signed_on': 'tenantSignedOn',
            'manager_signed_on': 'managerSignedOn',
            'signed_by_id': 'signedById',
            'signed_by__name': 'signedBy.name',
            'renewal_reminder_date': 'renewalReminderDate',
            'auto_reminder_enabled': 'autoReminderEnabled',
            'agreement_notes': 'agreementNotes',
            'key_number': 'keyNumber',
            'key_type': 'keyType',
            'key_available': 'keyAvailable',
            'key_booking_date': 'keyBookingDate',
            'confirmation_received': 'confirmationReceived',
            'key_delivery_date': 'keyDeliveryDate',
            'key_handover_status': 'keyHandoverStatus',
            'expected_handover_date': 'expectedHandoverDate',
            'handover_notes': 'handoverNotes',
            'tenant_confirmation_notes': 'tenantConfirmationNotes',
            'key_booked_on': 'keyBookedOn',
            'key_booked_by_id': 'keyBookedById',
            'key_booked_by__name': 'keyBookedBy.name',
            'key_prepared_on': 'keyPreparedOn',
            'key_notified_on': 'keyNotifiedOn',
            'handover_completed_on': 'handoverCompletedOn',
            'handed_over_by_id': 'handedOverById',
            'handed_over_by__name': 'handedOverBy.name',
            'internal_comments': 'internalComments',
            'tenant_remarks': 'tenantRemarks',
            'special_instructions': 'specialInstructions',
            'property_created_date': 'propertyCreatedDate',
            'listed_for_rent_date': 'listedForRentDate',
            'tenant_assigned_date': 'tenantAssignedDate',
            'assigned_to_employee_date': 'assignedToEmployeeDate',
            'property_occupied_date': 'propertyOccupiedDate',
            'created_by_id': 'createdById',
            'created_by__name': 'createdBy.name',
            'updated_by_id': 'updatedById',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'status_history': 'statusHistory',
            'is_active': 'isActive',
        }

    @staticmethod
    def flatten_to_nested_dict(df):
        result = []

        import numpy as np

        df = df.applymap(lambda x: x.isoformat() if isinstance(x, pandas.Timestamp) else (None if pandas.isna(x) else x))

        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})

        for _, row in df.iterrows():
            row_dict = {}
            for col, val in row.items():
                leaf_name = col.split(".")[-1]
                if isinstance(val, float) and val.is_integer() and leaf_name.endswith("Id"):
                    val = int(val)
                if "." in col:
                    parts = col.split(".")
                    current = row_dict
                    for part in parts[:-1]:
                        current = current.setdefault(part, {})
                    current[parts[-1]] = val
                else:
                    row_dict[col] = val
            result.append(row_dict)

        return result, df

    def mapper(self, data: list) -> str | None:
        if not data:
            return '[]'

        dataframe = pandas.DataFrame.from_records(data)

        if self.columns_required:
            Common.mapper_value_error(
                mapped_column_names=self.mapped_columns_name,
                columns_required=self.columns_required
            )
            reverse_map = {v: k for k, v in self.mapped_columns_name.items()}
            db_columns = [reverse_map.get(col, col) for col in self.columns_required]
            dataframe = dataframe[db_columns]

        dataframe.rename(columns=self.mapped_columns_name, inplace=True)

        flatten_data, cleaned_df = self.flatten_to_nested_dict(dataframe)
        return json.dumps(flatten_data, default=str)

    @staticmethod
    def reverse_mapper(fields: list[str]) -> dict[str, str]:
        reverse_map = {v: k for k, v in CheckInUtils().mapped_columns_name.items()}
        return {field: reverse_map.get(field, '') for field in fields}


class CheckOutUtils:
    def __init__(self, columns_required: list = []) -> None:
        self.columns_required = columns_required
        self.mapped_columns_name = {
            'check_out_id': 'checkOutId',
            'check_out_code': 'checkOutCode',
            'check_out_date': 'checkOutDate',
            'check_out_status': 'checkOutStatus',
            'remarks_notes': 'remarksNotes',
            'request_from': 'requestFrom',
            'tenant_code': 'tenantCode',
            'property_id': 'propertyId',
            'property_assignment_id': 'propertyAssignmentId',
            'check_in_id': 'checkInId',
            'tenant_id': 'tenantId',
            'assigned_employee_id': 'assignedEmployeeId',
            'assigned_employee__name': 'assignedEmployee.name',
            'tenant_code': 'tenantCode',
            'tenant_name': 'tenantName',
            'tenant_type': 'tenantType',
            'tenant_mobile_number': 'tenantMobileNumber',
            'tenant_email': 'tenantEmail',
            'tenant_civil_id': 'tenantCivilId',
            'tenant_passport_number': 'tenantPassportNumber',
            'tenant_nationality': 'tenantNationality',
            'tenant_address': 'tenantAddress',
            'date_of_birth': 'dateOfBirth',
            'gender': 'gender',
            'marital_status': 'maritalStatus',
            'emergency_contact_name': 'emergencyContactName',
            'emergency_contact_number': 'emergencyContactNumber',
            'profession': 'profession',
            'company_name': 'companyName',
            'property_type': 'propertyType',
            'property_code': 'propertyCode',
            'building_name': 'buildingName',
            'flat_unit_number': 'flatUnitNumber',
            'floor_number': 'floorNumber',
            'property_status': 'propertyStatus',
            'monthly_rent': 'monthlyRent',
            'security_deposit': 'securityDeposit',
            'advance_rent_received': 'advanceRentReceived',
            'first_month_rent_paid': 'firstMonthRentPaid',
            'payment_mode': 'paymentMode',
            'maintenance_charges': 'maintenanceCharges',
            'inspection_required': 'inspectionRequired',
            'inspection_date': 'inspectionDate',
            'technician_type': 'technicianType',
            'manager_approval': 'managerApproval',
            'inspection_priority': 'inspectionPriority',
            'issue_identified': 'issueIdentified',
            'supervisor_remarks': 'supervisorRemarks',
            'repair_required': 'repairRequired',
            'quotation_amount': 'quotationAmount',
            'inventory_available': 'inventoryAvailable',
            'gm_approval': 'gmApproval',
            'landlord_consent': 'landlordConsent',
            'finance_alert_generated': 'financeAlertGenerated',
            'rent_adjustment_amount': 'rentAdjustmentAmount',
            'repair_priority': 'repairPriority',
            'electricity_meter_reading': 'electricityMeterReading',
            'water_meter_reading': 'waterMeterReading',
            'gas_meter_reading': 'gasMeterReading',
            'charge_type': 'chargeType',
            'total_amount': 'totalAmount',
            'payment_status': 'paymentStatus',
            'payment_date': 'paymentDate',
            'transaction_id': 'transactionId',
            'settlement_status': 'settlementStatus',
            'finance_description': 'financeDescription',
            'payment_proof': 'paymentProof',
            'key_number': 'keyNumber',
            'key_type': 'keyType',
            'key_available': 'keyAvailable',
            'key_return': 'keyReturn',
            'expected_return_date': 'expectedReturnDate',
            'confirmation_received': 'confirmationReceived',
            'key_return_date': 'keyReturnDate',
            'key_return_status': 'keyReturnStatus',
            'internal_comments': 'internalComments',
            'tenant_remarks': 'tenantRemarks',
            'special_instructions': 'specialInstructions',
            'created_by_id': 'createdById',
            'created_by__name': 'createdBy.name',
            'updated_by_id': 'updatedById',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'status_history': 'statusHistory',
            'is_active': 'isActive',
        }

    def mapper(self, data: list) -> str | None:
        if not data:
            return '[]'

        dataframe = pandas.DataFrame.from_records(data)

        if self.columns_required:
            Common.mapper_value_error(
                mapped_column_names=self.mapped_columns_name,
                columns_required=self.columns_required
            )
            reverse_map = {v: k for k, v in self.mapped_columns_name.items()}
            db_columns = [reverse_map.get(col, col) for col in self.columns_required]
            dataframe = dataframe[db_columns]

        dataframe.rename(columns=self.mapped_columns_name, inplace=True)

        flatten_data, cleaned_df = CheckInUtils.flatten_to_nested_dict(dataframe)
        return json.dumps(flatten_data, default=str)

    @staticmethod
    def reverse_mapper(fields: list[str]) -> dict[str, str]:
        reverse_map = {v: k for k, v in CheckOutUtils().mapped_columns_name.items()}
        return {field: reverse_map.get(field, '') for field in fields}
