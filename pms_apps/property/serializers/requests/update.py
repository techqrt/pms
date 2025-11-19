from rest_framework import serializers
from pms_apps.authentication.serializers.request.create import PropertyUserSerializer
from pms_apps.property.dataclasses.requests.update import PropertyUpdateRequest


class UserRequestSerilizer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False,allow_null=True)

class PropertyUpdateSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    block = serializers.CharField(max_length = 10,required = False)
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
    assigned_to = UserRequestSerilizer(required=False,allow_null=True)

    def create(self, validated_data) -> PropertyUpdateRequest:
        assigned_user_data = validated_data.pop('assigned_to',{})

        assigned_to_user_id = assigned_user_data.get('user_id',None)
        return PropertyUpdateRequest(
            **validated_data,
            assigned_to=assigned_to_user_id
            )