from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.update.update_technician import MaintenanceTechnicianUpdateRequest, MaintenancePermissionUpdateRequest
from pms_apps.maintenance.serializers.request.create.create_manager import MaintenancePermissionRequestSerializer

class MaintenanceTechnicianUpdateRequestSerializer(serializers.Serializer):
    technician_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    skill_type = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    assigned_jobs = serializers.IntegerField(required=False, default=0)
    permissions = MaintenancePermissionRequestSerializer(required=False)

    def create(self, validated_data) -> MaintenanceTechnicianUpdateRequest:
        if 'permissions' in validated_data and validated_data['permissions']:
            permission_data = validated_data.pop('permissions')
            validated_data['permissions'] = MaintenancePermissionUpdateRequest(**permission_data)
        return MaintenanceTechnicianUpdateRequest(**validated_data)