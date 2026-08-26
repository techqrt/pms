from rest_framework import serializers

from pms_apps.property.dataclasses.requests.building_create import BuildingCreateRequest


class BuildingCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    block = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    total_floors = serializers.IntegerField(required=False, allow_null=True)
    year_of_construction = serializers.IntegerField(required=False, allow_null=True)

    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    area_zone = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    pincode = serializers.CharField(max_length=10)
    google_map_location = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    internal_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> BuildingCreateRequest:
        return BuildingCreateRequest(**validated_data)
