from rest_framework import serializers
from pms_apps.common.serializers.response.api_response import APiResponseSerializer
from pms_apps.common.serializers.response.get_all import GetAllGeneralSerializer
from pms_apps.authentication.serializers.response.get_all import PropertyUserSerializer


class PropertyDataSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    building_details = serializers.CharField(required=False, allow_blank=True)
    floor = serializers.CharField(required=False, allow_blank=True)
    flat_number = serializers.IntegerField(required=False, allow_null=True)
    dimension_length_ft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    dimension_breadth_ft = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    dimension_area_sqft = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    rental_type = serializers.CharField(required=False, allow_blank=True)
    hall = serializers.BooleanField(required=False)
    bedroom_count = serializers.IntegerField(required=False)
    kitchen = serializers.BooleanField(required=False)
    attached_bathroom_count = serializers.IntegerField(required=False)
    single_bathroom_count = serializers.IntegerField(required=False)
    balcony = serializers.BooleanField(required=False)
    store_room = serializers.BooleanField(required=False)
    rental_for = serializers.CharField(required=False, allow_blank=True)
    advance_amount_rent = serializers.IntegerField(required=False, allow_null=True)
    expected_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    agreement_id = serializers.IntegerField(required=False, allow_null=True)
    photos = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)
    videos = serializers.ListField(child=serializers.URLField(), required=False, allow_null=True)
    created_by = PropertyUserSerializer()
    assigned_to = PropertyUserSerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_active = serializers.BooleanField()



class PropertyGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=PropertyDataSerializer())

class PropertyGetAllResponseSerializer(APiResponseSerializer):
    data = PropertyGetAllSerializer()
