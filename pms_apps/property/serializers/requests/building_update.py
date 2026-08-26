from rest_framework import serializers

from pms_apps.property.dataclasses.requests.building_update import BuildingUpdateRequest


class BuildingUpdateSerializer(serializers.Serializer):
    building_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    block = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    total_floors = serializers.IntegerField(required=False, allow_null=True)
    year_of_construction = serializers.IntegerField(required=False, allow_null=True)

    address_line_1 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    address_line_2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    area_zone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    pincode = serializers.CharField(max_length=10, required=False, allow_null=True, allow_blank=True)
    google_map_location = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    internal_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> BuildingUpdateRequest:
        return BuildingUpdateRequest(**validated_data)
