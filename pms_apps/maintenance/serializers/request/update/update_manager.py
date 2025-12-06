from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.update.update_manager import MaintenanceManagerUpdateRequest

class MaintenanceManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> MaintenanceManagerUpdateRequest:
        return MaintenanceManagerUpdateRequest(**validated_data)