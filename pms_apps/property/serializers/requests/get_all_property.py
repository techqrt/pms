from datetime import datetime, time

from django.utils import timezone
from rest_framework import serializers

from pms.config import Configurations
from pms_apps.property.dataclasses.requests.get_all_property import PropertyGetAllRequest


class PropertyGetAllSerializer(serializers.Serializer):
    values = serializers.CharField(max_length=100, required=False, default='')
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)
    sort_by = serializers.CharField(max_length=100, required=False, default='')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    search_key = serializers.CharField(max_length=100, required=False, default='')
    property_types = serializers.CharField(
        required=False, default='',
        help_text='Comma separated: Apartment,Villa,Warehouse,Commercial'
    )
    rental_for = serializers.CharField(
        required=False, default='',
        help_text='Comma separated: Bachelor,Family,Labour'
    )
    bedrooms = serializers.CharField(
        required=False, default='',
        help_text='Comma separated BHK values: 1BHK,2BHK,3BHK'
    )
    features = serializers.CharField(
        required=False, default='',
        help_text='Comma separated: Balcony,Parking,Pool'
    )
    building_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    city = serializers.CharField(max_length=100, required=False, default='')
    min_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True, default=None)
    max_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True, default=None)
    from_date = serializers.DateField(input_formats=["%d-%m-%y"], required=False, allow_null=True, default=None)
    to_date = serializers.DateField(input_formats=["%d-%m-%y"], required=False, allow_null=True, default=None)

    def create(self, validated_data) -> PropertyGetAllRequest:
        from_date = validated_data.pop('from_date', None)
        to_date = validated_data.pop('to_date', None)
        if from_date:
            from_date = timezone.make_aware(datetime.combine(from_date, time.min))
        if to_date:
            to_date = timezone.make_aware(datetime.combine(to_date, time.max))

        property_types = validated_data.pop('property_types', '') or ''
        rental_for = validated_data.pop('rental_for', '') or ''
        bedrooms = validated_data.pop('bedrooms', '') or ''
        features = validated_data.pop('features', '') or ''

        return PropertyGetAllRequest(
            property_types=[t.strip() for t in property_types.split(',') if t.strip()],
            rental_for=[t.strip() for t in rental_for.split(',') if t.strip()],
            bedrooms=[t.strip() for t in bedrooms.split(',') if t.strip()],
            features=[t.strip() for t in features.split(',') if t.strip()],
            from_date=from_date,
            to_date=to_date,
            **validated_data
        )
