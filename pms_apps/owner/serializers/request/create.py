from rest_framework import serializers
from pms_apps.owner.dataclasses.request.create import OwnerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class OwnerCreateRequestSerializer(serializers.Serializer):
    owner_id = UserRequestSerializer()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    ownership_type = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    properties_owned = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> OwnerCreateRequest:
        owner_id_data = validated_data.pop('owner_id')
        validated_data['owner_id'] = owner_id_data['user_id']

        return OwnerCreateRequest(**validated_data)