from rest_framework import serializers
from pms_apps.maintenance.serializers.request.create.create_manager import UserRequestSerializer
from pms_apps.maintenance.dataclasses.request.create.create_technician import MaintenanceTechnicianCreateRequest

class MaintenanceTechnicianCreateRequestSerializer(serializers.Serializer):
    technician_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    skill_type = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    assigned_jobs = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> MaintenanceTechnicianCreateRequest:
        technician_id_data = validated_data.pop('technician_id')
        validated_data['technician_id'] = technician_id_data['user_id']

        return MaintenanceTechnicianCreateRequest(**validated_data)