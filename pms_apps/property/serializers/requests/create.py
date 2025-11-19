from rest_framework import serializers
from pms_apps.property.dataclasses.requests.create import PropertyCreateRequest as PropertyCreateRequest
from pms_apps.authentication.serializers.request.create import PropertyUserSerializer

class UserRequestSerilizer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False,allow_null=True)

class PropertyCreateSerializer(serializers.Serializer):
    block = serializers.CharField()
    building_details = serializers.CharField()
    floor = serializers.CharField()
    flat_number = serializers.IntegerField()
    dimension_length_ft = serializers.DecimalField(max_digits=10, decimal_places=2)
    dimension_breadth_ft = serializers.DecimalField(max_digits=10, decimal_places=2)
    dimension_area_sqft = serializers.DecimalField(max_digits=12, decimal_places=2)
    rental_type = serializers.ChoiceField(choices=["Residential", "Commercial"])
    hall = serializers.BooleanField()
    bedroom_count = serializers.IntegerField()
    kitchen = serializers.BooleanField()
    attached_bathroom_count = serializers.IntegerField()
    single_bathroom_count = serializers.IntegerField()
    balcony = serializers.BooleanField()
    store_room = serializers.BooleanField()
    rental_for = serializers.ChoiceField(choices=["Bachelor", "Family", "Labour"])
    advance_amount_rent = serializers.IntegerField()
    expected_rent = serializers.DecimalField(max_digits=12, decimal_places=2)
    agreement_id = serializers.IntegerField()
    photos = serializers.ListField(child=serializers.URLField())
    videos = serializers.ListField(child=serializers.URLField())
    assigned_to = UserRequestSerilizer(required=False,allow_null=True)

    def create(self, validated_data) -> PropertyCreateRequest:
        return PropertyCreateRequest(
            **validated_data,
            )