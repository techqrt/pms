from rest_framework import serializers
from pms_apps.maintenance.dataclasses.request.create.create_manager import MaintenanceManagerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class MaintenanceManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    specialization = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> MaintenanceManagerCreateRequest:
        manager_id_data = validated_data.pop('manager_id')
        validated_data['manager_id'] = manager_id_data['user_id']

        return MaintenanceManagerCreateRequest(**validated_data)