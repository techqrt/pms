from rest_framework import serializers
from pms_apps.marketing.serializers.request.create.create_manager import  UserRequestSerializer,MarketingPermissionRequestSerializer

from pms_apps.marketing.dataclasses.request.create.create_employee import MarketingEmployeeCreateRequest

from pms_apps.common.dataclasses.request.permission import Permissions


class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()


class MarketingEmployeeCreateRequestSerializer(serializers.Serializer):
    employee_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True
    )
    department = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True
    )
    campaigns_assigned = serializers.IntegerField(required=False, default=0)
    leads_generated = serializers.IntegerField(required=False, default=0)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)
    permissions = MarketingPermissionRequestSerializer()

    def create(self, validated_data) -> MarketingEmployeeCreateRequest:
        employee_data = validated_data.pop("employee_id")
        permission_data = validated_data.pop("permissions")

        manager_ref_data = validated_data.pop("manager_ref", None)

        employee_id = employee_data["user_id"]
        permission = Permissions(**permission_data)

        manager_ref = (
            manager_ref_data["manager_id"]
            if manager_ref_data is not None
            else None
        )

        return MarketingEmployeeCreateRequest(
            employee_id=employee_id,
            manager_ref=manager_ref,
            permissions=permission,
            **validated_data
        )
