from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.update.update_technician import MaintenanceTechnicianUpdateRequest

class MaintenanceTechnicianUpdateRequestSerializer(serializers.Serializer):
    technician_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    skill_type = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    assigned_jobs = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> MaintenanceTechnicianUpdateRequest:
        return MaintenanceTechnicianUpdateRequest(**validated_data)