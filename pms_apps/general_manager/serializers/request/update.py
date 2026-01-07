from rest_framework import serializers
from pms_apps.general_manager.dataclasses.request.update import GeneralManagerUpdateRequest

class GeneralManagerUpdateRequestSerializer(serializers.Serializer):
    general_manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    years_of_experience = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> GeneralManagerUpdateRequest:
        return GeneralManagerUpdateRequest(**validated_data)