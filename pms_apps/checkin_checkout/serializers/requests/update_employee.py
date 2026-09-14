from rest_framework import serializers

from pms_apps.checkin_checkout.dataclasses.requests.update_employee import CheckInCheckOutEmployeeUpdateRequest
from pms_apps.checkin_checkout.dataclasses.requests.update_manager import CheckInCheckOutPermissionUpdateRequest
from pms_apps.checkin_checkout.serializers.requests.update_manager import CheckInCheckOutPermissionRequestSerializer


class CheckInCheckOutEmployeeUpdateRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    manager_ref = serializers.IntegerField(required=False, allow_null=True)
    permissions = CheckInCheckOutPermissionRequestSerializer(required=False)

    def create(self, validated_data) -> CheckInCheckOutEmployeeUpdateRequest:
        if validated_data.get('permissions'):
            permission_data = validated_data.pop('permissions')
            validated_data['permissions'] = CheckInCheckOutPermissionUpdateRequest(**permission_data)
        else:
            validated_data.pop('permissions', None)
        return CheckInCheckOutEmployeeUpdateRequest(**validated_data)
