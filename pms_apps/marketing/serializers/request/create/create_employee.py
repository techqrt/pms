from rest_framework import serializers
from pms_apps.marketing.serializers.request.create.create_manager import UserRequestSerializer
from pms_apps.marketing.dataclasses.request.create.create_employee import MarketingEmployeeCreateRequest
from pms_apps.marketing.dataclasses.request.create.create_manager import MarketingPermissionCreateRequest
from pms_apps.marketing.serializers.request.create.create_manager import MarketingPermissionRequestSerializer


class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()


class MarketingEmployeeCreateRequestSerializer(serializers.Serializer):
    employee_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    department = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    campaigns_assigned = serializers.IntegerField(required=False, default=0)
    leads_generated = serializers.IntegerField(required=False, default=0)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)
    permission = MarketingPermissionRequestSerializer()

    def create(self, validated_data) -> MarketingEmployeeCreateRequest:
        employee_id_data = validated_data.pop('employee_id')
        validated_data['employee_id'] = employee_id_data['user_id']

        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        permission_data = validated_data.pop('permission')
        validated_data['permission'] = MarketingPermissionCreateRequest(**permission_data)

        return MarketingEmployeeCreateRequest(**validated_data)
