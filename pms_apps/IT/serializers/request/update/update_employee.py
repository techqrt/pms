from rest_framework import serializers
from pms_apps.IT.dataclasses.request.update.update_employee import ITEmployeeUpdateRequest


class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()


class ITEmployeeUpdateRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    role_title = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    tickets_resolved = serializers.IntegerField(required=False, default=0)
    projects_assigned = serializers.IntegerField(required=False, default=0)
    specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)

    def create(self, validated_data) -> ITEmployeeUpdateRequest:
        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        return ITEmployeeUpdateRequest(**validated_data)
