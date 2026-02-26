from rest_framework import serializers
from pms_apps.reception.dataclasses.request.create.create_manager import ReceptionManagerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class ReceptionManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    team_size = serializers.IntegerField(required=False, default=0)
    front_desk_count = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> ReceptionManagerCreateRequest:
        manger_id_data = validated_data.pop('manager_id')
        validated_data['manager_id'] = manger_id_data['user_id']

        return ReceptionManagerCreateRequest(**validated_data)