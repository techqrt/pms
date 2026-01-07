from rest_framework import serializers
from pms_apps.legal.dataclasses.request.update.update_manager import LegalManagerUpdateRequest

class LegalManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    total_cases_handled = serializers.IntegerField(required=False, default=0)
    open_cases = serializers.IntegerField(required=False, default=0)
    closed_cases = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> LegalManagerUpdateRequest:
        return LegalManagerUpdateRequest(**validated_data)