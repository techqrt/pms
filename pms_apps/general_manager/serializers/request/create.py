from rest_framework import serializers
from pms_apps.general_manager.dataclasses.request.create import GeneralManagerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class GeneralManagerCreateRequestSerializer(serializers.Serializer):
    general_manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> GeneralManagerCreateRequest:
        general_manager_id_data = validated_data.pop('general_manager_id')
        validated_data['general_manager_id'] = general_manager_id_data['user_id']

        return GeneralManagerCreateRequest(**validated_data)