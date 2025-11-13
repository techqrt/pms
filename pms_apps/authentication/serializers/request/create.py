from rest_framework import serializers
from pms_apps.authentication.dataclasses.request.create import PropertyUserRequest  


class PropertyUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data) -> PropertyUserRequest:
        return PropertyUserRequest(**validated_data)
