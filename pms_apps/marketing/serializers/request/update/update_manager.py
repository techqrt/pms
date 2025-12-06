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
    permission = MarketingPermissionRequestSerializer(required=False)

    def create(self, validated_data) -> MarketingManagerUpdateRequest:
        if 'permission' in validated_data and validated_data['permission']:
            permission_data = validated_data.pop('permission')
            validated_data['permission'] = MarketingPermissionUpdateRequest(**permission_data)
        return MarketingManagerUpdateRequest(**validated_data)
