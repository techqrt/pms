from rest_framework import serializers
from pms_apps.property.dataclasses.requests.create import PropertyCreateRequest as PropertyCreateRequest
from pms_apps.authentication.serializers.request.create import PropertyUserSerializer


class PropertyCreateSerializer(serializers.Serializer):
    building_details = serializers.CharField(required=False, allow_blank=True)
    floor = serializers.CharField(required=False, allow_blank=True)
    flat_number = serializers.IntegerField(required=False)
    dimension_length_ft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    dimension_breadth_ft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    dimension_area_sqft = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    rental_type = serializers.ChoiceField(choices=["Residential", "Commercial"], required=False)
    hall = serializers.BooleanField(required=False)
    bedroom_count = serializers.IntegerField(required=False)
    kitchen = serializers.BooleanField(required=False)
    attached_bathroom_count = serializers.IntegerField(required=False)
    single_bathroom_count = serializers.IntegerField(required=False)
    balcony = serializers.BooleanField(required=False)
    store_room = serializers.BooleanField(required=False)
    rental_for = serializers.ChoiceField(choices=["Bachelor", "Family", "Labour"], required=False)
    advance_amount_rent = serializers.IntegerField(required=False)
    expected_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    agreement_id = serializers.IntegerField(required=False)
    photos = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)
    videos = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)
    created_by = PropertyUserSerializer()
    assigned_to = PropertyUserSerializer()

    def create(self, validated_data) -> PropertyCreateRequest:
        return PropertyCreateRequest(**validated_data)