from rest_framework import serializers
from pms_apps.maintenance.serializers.response.get.get_manager import UserGetSerializer
from pms_apps.maintenance.serializers.response.get.get_manager import PermissionGetSerializer

class MaintenanceTechnicianGetSerializer(serializers.Serializer):
    technicianId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    skillType = serializers.CharField(read_only=True)
    yearsOfExperience = serializers.IntegerField(read_only=True)
    assignedJobs = serializers.IntegerField(read_only=True)
    permission = PermissionGetSerializer(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)

class MaintenanceTechnicianResponseGetSerializer(serializers.Serializer):
    data = MaintenanceTechnicianGetSerializer()