from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.update.update_manager import MaintenanceManagerUpdateRequest, MaintenancePermissionUpdateRequest
from pms_apps.maintenance.serializers.request.create.create_manager import MaintenancePermissionRequestSerializer

class MaintenanceManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)
    permissions = MaintenancePermissionRequestSerializer(required=False)

    def create(self, validated_data) -> MaintenanceManagerUpdateRequest:
        if 'permissions' in validated_data and validated_data['permissions']:
            permission_data = validated_data.pop('permissions')
            validated_data['permissions'] = MaintenancePermissionUpdateRequest(**permission_data)
        return MaintenanceManagerUpdateRequest(**validated_data)