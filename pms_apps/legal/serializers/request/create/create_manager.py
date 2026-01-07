from rest_framework import serializers
from pms_apps.legal.dataclasses.request.create.create_manager import LegalManagerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class LegalManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    total_cases_handled = serializers.IntegerField(required=False, default=0)
    open_cases = serializers.IntegerField(required=False, default=0)
    closed_cases = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> LegalManagerCreateRequest:
        manager_id_data = validated_data.pop('manager_id')
        validated_data['manager_id'] = manager_id_data['user_id']

        return LegalManagerCreateRequest(**validated_data)
