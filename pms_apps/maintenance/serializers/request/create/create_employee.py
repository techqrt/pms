from rest_framework import serializers
from pms_apps.maintenance.serializers.request.create.create_manager import UserRequestSerializer
from pms_apps.maintenance.dataclasses.request.create.create_employee import MaintenanceEmployeeCreateRequest

class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

class MaintenanceEmployeeCreateRequestSerializer(serializers.Serializer):
    employee_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    assigned_tasks = serializers.IntegerField(required=False, default=0)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)

    def create(self, validated_data) -> MaintenanceEmployeeCreateRequest:
        employee_id_data = validated_data.pop('employee_id')
        validated_data['employee_id'] = employee_id_data['user_id']

        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        return MaintenanceEmployeeCreateRequest(**validated_data)