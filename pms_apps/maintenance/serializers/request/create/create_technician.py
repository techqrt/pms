from rest_framework import serializers
from pms_apps.maintenance.serializers.request.create.create_manager import UserRequestSerializer, MaintenancePermissionRequestSerializer
from pms_apps.maintenance.dataclasses.request.create.create_technician import MaintenanceTechnicianCreateRequest
from pms_apps.common.dataclasses.request.permission import PermissionsProperty

class MaintenanceTechnicianCreateRequestSerializer(serializers.Serializer):
    technician_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    skill_type = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    assigned_jobs = serializers.IntegerField(required=False, default=0)
    permissions = MaintenancePermissionRequestSerializer()

    def create(self, validated_data) -> MaintenanceTechnicianCreateRequest:
        user_data = validated_data.pop("technician_id")
        permission_data = validated_data.pop("permissions")

        technician_id = user_data["user_id"]
        permissions = PermissionsProperty(**permission_data)

        return MaintenanceTechnicianCreateRequest(technician_id=technician_id, permissions=permissions, **validated_data)