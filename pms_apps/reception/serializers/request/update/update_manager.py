from rest_framework import serializers
from pms_apps.reception.dataclasses.request.update.update_manager import ReceptionManagerUpdateRequest

class ReceptionManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    team_size = serializers.IntegerField(required=False, default=0)
    front_desk_count = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> ReceptionManagerUpdateRequest:
        return ReceptionManagerUpdateRequest(**validated_data)