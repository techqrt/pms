from rest_framework import serializers
from pms_apps.IT.dataclasses.request.create.create_manager import ITManagerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class ITManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    projects_managed = serializers.IntegerField(required=False, default=0)
    systems_overseen = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> ITManagerCreateRequest:
        manager_id_data = validated_data.pop('manager_id')
        validated_data['manager_id'] = manager_id_data['user_id']

        return ITManagerCreateRequest(**validated_data)
