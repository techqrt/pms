from rest_framework import serializers
from pms_apps.marketing.dataclasses.request.update.update_manager import MarketingManagerUpdateRequest
from pms_apps.marketing.dataclasses.request.update.update_manager import MarketingPermissionUpdateRequest
from pms_apps.marketing.serializers.request.create.create_manager import MarketingPermissionRequestSerializer


class MarketingManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    campaigns_led = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    profile_picture = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    permissions = MarketingPermissionRequestSerializer(required=False)
    old_password = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    new_password = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        if bool(old_password) != bool(new_password):
            raise serializers.ValidationError(
                "Both old_password and new_password are required to change the password"
            )
        return attrs

    def create(self, validated_data) -> MarketingManagerUpdateRequest:
        if 'permissions' in validated_data and validated_data['permissions']:
            permission_data = validated_data.pop('permissions')
            validated_data['permissions'] = MarketingPermissionUpdateRequest(**permission_data)
        return MarketingManagerUpdateRequest(**validated_data)
