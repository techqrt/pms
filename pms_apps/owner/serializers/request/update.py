from rest_framework import serializers
from pms_apps.owner.dataclasses.request.update import OwnerUpdateRequest

class OwnerUpdateRequestSerializer(serializers.Serializer):
    owner_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    ownership_type = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    properties_owned = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> OwnerUpdateRequest:
        return OwnerUpdateRequest(**validated_data)