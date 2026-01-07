from rest_framework import serializers
from pms_apps.IT.dataclasses.request.update.update_manager import ITManagerUpdateRequest


class ITManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True)
    projects_managed = serializers.IntegerField(required=False, default=0)
    systems_overseen = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> ITManagerUpdateRequest:
        return ITManagerUpdateRequest(**validated_data)
