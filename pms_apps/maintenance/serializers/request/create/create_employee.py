from rest_framework import serializers
from pms_apps.maintenance.serializers.request.create.create_manager import UserRequestSerializer, MaintenancePermissionRequestSerializer
from pms_apps.maintenance.dataclasses.request.create.create_employee import MaintenanceEmployeeCreateRequest
from pms_apps.common.dataclasses.request.permission import PermissionsProperty

class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

class MaintenanceEmployeeCreateRequestSerializer(serializers.Serializer):
    employee_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    assigned_tasks = serializers.IntegerField(required=False, default=0)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)
    permissions = MaintenancePermissionRequestSerializer()

    def create(self, validated_data) -> MaintenanceEmployeeCreateRequest:
        employee_data = validated_data.pop("employee_id")
        permission_data = validated_data.pop("permissions")

        manager_ref_data = validated_data.pop("manager_ref", None)

        employee_id = employee_data["user_id"]
        permission = PermissionsProperty(**permission_data)

        manager_ref = (
            manager_ref_data["manager_id"]
            if manager_ref_data is not None
            else None
        )

        return MaintenanceEmployeeCreateRequest(
            employee_id=employee_id,
            manager_ref=manager_ref,
            permissions=permission,
            **validated_data
        )