from rest_framework import serializers

from pms_apps.checkin_checkout.dataclasses.requests.respond_check_in_request import CheckInRequestRespondRequest


class CheckInRequestRespondSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    accept = serializers.BooleanField(default=False)
    reject = serializers.BooleanField(default=False)
    rejection_reason = serializers.CharField(
        max_length=500, required=False, allow_blank=True, allow_null=True, default=None
    )

    def validate(self, attrs):
        if attrs.get('accept') == attrs.get('reject'):
            raise serializers.ValidationError("Exactly one of 'accept' or 'reject' must be true.")
        return attrs

    def create(self, validated_data) -> CheckInRequestRespondRequest:
        return CheckInRequestRespondRequest(**validated_data)
