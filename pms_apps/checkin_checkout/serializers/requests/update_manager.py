from rest_framework import serializers

from pms_apps.checkin_checkout.dataclasses.requests.update_manager import (
    CheckInCheckOutManagerUpdateRequest,
    CheckInCheckOutPermissionUpdateRequest,
)


class CheckInCheckOutPermissionRequestSerializer(serializers.Serializer):
    lead = serializers.BooleanField(required=False)
    property = serializers.BooleanField(required=False)


class CheckInCheckOutManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    team_size = serializers.IntegerField(required=False, allow_null=True)
    permissions = CheckInCheckOutPermissionRequestSerializer(required=False)

    def create(self, validated_data) -> CheckInCheckOutManagerUpdateRequest:
        if validated_data.get('permissions'):
            permission_data = validated_data.pop('permissions')
            validated_data['permissions'] = CheckInCheckOutPermissionUpdateRequest(**permission_data)
        else:
            validated_data.pop('permissions', None)
        return CheckInCheckOutManagerUpdateRequest(**validated_data)
