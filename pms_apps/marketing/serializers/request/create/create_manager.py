from rest_framework import serializers
from pms_apps.marketing.dataclasses.request.create.create_manager import MarketingManagerCreateRequest
from pms_apps.marketing.dataclasses.request.create.create_manager import MarketingPermissionCreateRequest


class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class MarketingPermissionRequestSerializer(serializers.Serializer):
    lead = serializers.BooleanField()
    property = serializers.BooleanField()


class MarketingManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    campaigns_led = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)
    permission = MarketingPermissionRequestSerializer()

    def create(self, validated_data) -> MarketingManagerCreateRequest:
        manager_id_data = validated_data.pop('manager_id')
        validated_data['manager_id'] = manager_id_data['user_id']

        permission_data = validated_data.pop('permission')
        validated_data['permission'] = MarketingPermissionCreateRequest(
            **permission_data)

        return MarketingManagerCreateRequest(**validated_data)
