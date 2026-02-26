from rest_framework import serializers
from pms_apps.legal.dataclasses.request.update.update_employee import LegalEmployeeUpdateRequest


class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

class LegalEmployeeUpdateRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    active_cases = serializers.IntegerField(required=False, default=0)
    case_specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)

    def create(self, validated_data) -> LegalEmployeeUpdateRequest:
        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        return LegalEmployeeUpdateRequest(**validated_data)