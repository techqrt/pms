from rest_framework import serializers
from pms_apps.property.dataclasses.requests.property_assignment_create import PropertyAssignmentCreateRequest


class PropertyAssignmentCreateSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    tenant_id = serializers.IntegerField()
    assigned_by_id = serializers.IntegerField()
    assignment_status = serializers.ChoiceField(
        choices=["Pending", "Approved", "Active", "Completed", "Cancelled"],
        default="Pending"
    )
    company_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    rental_start_date = serializers.DateField(required=False, allow_null=True)
    rental_end_date = serializers.DateField(required=False, allow_null=True)
    agreement_duration_months = serializers.IntegerField(required=False, allow_null=True)
    maintenance_charges = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    advance_rent_paid = serializers.BooleanField(default=False)
    payment_mode = serializers.ChoiceField(
        choices=["Cash", "Bank Transfer", "Online", "Cheque"],
        required=False,
        allow_null=True
    )
    agreement_type = serializers.ChoiceField(
        choices=["Government Agreement", "Internal Agreement"],
        required=False,
        allow_null=True
    )
    agreement_status = serializers.ChoiceField(
        choices=["Pending", "Prepared", "Signed", "Executed", "Terminated"],
        default="Pending"
    )
    agreement_prepared_by_id = serializers.IntegerField(required=False, allow_null=True)
    key_available_in_office = serializers.ChoiceField(
        choices=["Yes", "No"],
        default="No"
    )
    key_code = serializers.CharField(max_length=100, required=False, allow_null=True)
    key_handover_date = serializers.DateField(required=False, allow_null=True)
    key_handover_status = serializers.ChoiceField(
        choices=["Pending", "Handed Over", "Returned"],
        default="Pending"
    )
    electricity_meter_number = serializers.CharField(max_length=100, required=False, allow_null=True)
    electricity_meter_reading_start = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    water_meter_reading_start = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    gas_meter_reading_start = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    finance_approval_status = serializers.ChoiceField(
        choices=["Pending", "Approved", "On Hold", "Rejected"],
        default="Pending"
    )
    rent_entry_created = serializers.ChoiceField(
        choices=["No", "Yes"],
        default="No"
    )
    invoice_generated = serializers.ChoiceField(
        choices=["No", "Yes"],
        default="No"
    )
    maintenance_required = serializers.ChoiceField(
        choices=["No", "Yes"],
        default="No"
    )
    maintenance_ticket_id = serializers.CharField(max_length=100, required=False, allow_null=True)
    maintenance_status = serializers.ChoiceField(
        choices=["Pending", "In Progress", "Completed", "Not Required"],
        default="Pending"
    )
    internal_notes = serializers.CharField(required=False, default="", allow_blank=True)
    tenant_special_requirements = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> PropertyAssignmentCreateRequest:
        return PropertyAssignmentCreateRequest(
            property_id=validated_data['property_id'],
            tenant_id=validated_data['tenant_id'],
            assigned_by_id=validated_data['assigned_by_id'],
            assignment_status=validated_data.get('assignment_status', 'Pending'),
            company_name=validated_data.get('company_name'),
            rental_start_date=validated_data.get('rental_start_date'),
            rental_end_date=validated_data.get('rental_end_date'),
            agreement_duration_months=validated_data.get('agreement_duration_months'),
            maintenance_charges=validated_data.get('maintenance_charges'),
            advance_rent_paid=validated_data.get('advance_rent_paid', False),
            payment_mode=validated_data.get('payment_mode'),
            agreement_type=validated_data.get('agreement_type'),
            agreement_status=validated_data.get('agreement_status', 'Pending'),
            agreement_prepared_by_id=validated_data.get('agreement_prepared_by_id'),
            key_available_in_office=validated_data.get('key_available_in_office', 'No'),
            key_code=validated_data.get('key_code'),
            key_handover_date=validated_data.get('key_handover_date'),
            key_handover_status=validated_data.get('key_handover_status', 'Pending'),
            electricity_meter_number=validated_data.get('electricity_meter_number'),
            electricity_meter_reading_start=validated_data.get('electricity_meter_reading_start'),
            water_meter_reading_start=validated_data.get('water_meter_reading_start'),
            gas_meter_reading_start=validated_data.get('gas_meter_reading_start'),
            finance_approval_status=validated_data.get('finance_approval_status', 'Pending'),
            rent_entry_created=validated_data.get('rent_entry_created', 'No'),
            invoice_generated=validated_data.get('invoice_generated', 'No'),
            maintenance_required=validated_data.get('maintenance_required', 'No'),
            maintenance_ticket_id=validated_data.get('maintenance_ticket_id'),
            maintenance_status=validated_data.get('maintenance_status', 'Pending'),
            internal_notes=validated_data.get('internal_notes', ''),
            tenant_special_requirements=validated_data.get('tenant_special_requirements', ''),
        )
