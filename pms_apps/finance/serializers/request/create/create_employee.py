from rest_framework import serializers
from pms_apps.finance.serializers.request.create.create_manager import UserRequestSerializer
from pms_apps.finance.dataclasses.request.create.create_employee import FinanceEmployeeCreateRequest

class ManagerRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()

class FinanceEmployeeCreateRequestSerializer(serializers.Serializer):
    employee_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    role_title = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    invoices_processed = serializers.IntegerField(required=False, default=0)
    payments_verified = serializers.IntegerField(required=False, default=0)
    total_amount_handled = serializers.DecimalField(required=False, default=0.0, max_digits=20, decimal_places=2)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)

    def create(self, validated_data) -> FinanceEmployeeCreateRequest:
        employee_id_data = validated_data.pop('employee_id')
        validated_data['employee_id'] = employee_id_data['user_id']

        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        return FinanceEmployeeCreateRequest(**validated_data)