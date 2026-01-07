from rest_framework import serializers
from pms_apps.IT.dataclasses.request.update.update_technician import ITTechnicianUpdateRequest

class ITTechnicianUpdateRequestSerializer(serializers.Serializer):
    technician_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    skill_area = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    tickets_closed = serializers.IntegerField(required=False, default=0)
    years_of_experience = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> ITTechnicianUpdateRequest:
        return ITTechnicianUpdateRequest(**validated_data)