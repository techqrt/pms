from rest_framework import serializers
from pms_apps.marketing.dataclasses.request.update.update_employee import MarketingEmployeeUpdateRequest
from pms_apps.marketing.dataclasses.request.update.update_manager import MarketingPermissionUpdateRequest
from pms_apps.marketing.serializers.request.create.create_manager import MarketingPermissionRequestSerializer


class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()


class MarketingEmployeeUpdateRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    department = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    campaigns_assigned = serializers.IntegerField(required=False, default=0)
    leads_generated = serializers.IntegerField(required=False, default=0)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)
    permission = MarketingPermissionRequestSerializer(required=False)

    def create(self, validated_data) -> MarketingEmployeeUpdateRequest:
        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        if 'permission' in validated_data and validated_data['permission']:
            permission_data = validated_data.pop('permission')
            validated_data['permission'] = MarketingPermissionUpdateRequest(**permission_data)

        return MarketingEmployeeUpdateRequest(**validated_data)
