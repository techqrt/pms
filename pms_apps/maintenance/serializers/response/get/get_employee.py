from rest_framework import serializers
from pms_apps.maintenance.serializers.response.get.get_manager import UserGetSerializer
from pms_apps.maintenance.serializers.response.get.get_manager import PermissionGetSerializer

class MaintenanceManagerRefGetSerializer(serializers.Serializer):
    managerId = serializers.IntegerField()


class MaintenanceEmployeeGetSerializer(serializers.Serializer):
    employeeId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    designation = serializers.CharField(read_only=True)
    specialization = serializers.CharField(read_only=True)
    assignedTasks = serializers.IntegerField(read_only=True)
    managerRef = MaintenanceManagerRefGetSerializer(required=False)
    permission = PermissionGetSerializer(required=False)
    createdAt = serializers.DateTimeField(read_only=True)


class MaintenanceEmployeeResponseGetSerializer(serializers.Serializer):
    data = MaintenanceEmployeeGetSerializer()
