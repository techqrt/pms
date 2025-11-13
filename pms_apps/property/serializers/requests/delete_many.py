from rest_framework import serializers

from pms_apps.property.dataclasses.requests.delete_many import PropertyDeleteManyRequest


class PropertyDeleteManySerializer(serializers.Serializer):
    property_id = serializers.ListField(required=True)

    def create(self, validated_data) -> PropertyDeleteManyRequest:
        return PropertyDeleteManyRequest(**validated_data)
