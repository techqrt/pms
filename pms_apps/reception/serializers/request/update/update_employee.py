from rest_framework import serializers
from pms_apps.reception.dataclasses.request.update.update_employee import ReceptionEmployeeUpdateRequest

class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

class ReceptionEmployeeUpdateRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    shift = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    desk_number = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    calls_handled = serializers.IntegerField(required=False, default=0)
    visitors_logged = serializers.IntegerField(required=False, default=0)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)

    def create(self, validated_data) -> ReceptionEmployeeUpdateRequest:
        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        return ReceptionEmployeeUpdateRequest(**validated_data)