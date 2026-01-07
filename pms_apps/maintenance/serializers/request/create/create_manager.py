from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.create.create_manager import MaintenanceManagerCreateRequest
from pms_apps.common.dataclasses.request.permission import PermissionsProperty

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class MaintenancePermissionRequestSerializer(serializers.Serializer):
    property = serializers.BooleanField()

class MaintenanceManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)
    permissions = MaintenancePermissionRequestSerializer()

    def create(self, validated_data) -> MaintenanceManagerCreateRequest:
        user_data = validated_data.pop("manager_id")
        permission_data = validated_data.pop("permissions")

        manager_id = user_data["user_id"]
        permissions = PermissionsProperty(**permission_data)

        return MaintenanceManagerCreateRequest(manager_id=manager_id, permissions=permissions, **validated_data)