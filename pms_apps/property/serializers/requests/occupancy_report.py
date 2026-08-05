from datetime import datetime, time

from django.utils import timezone
from rest_framework import serializers

from pms.config import Configurations
from pms_apps.property.dataclasses.requests.occupancy_report import OccupancyReportRequest


class OccupancyReportSerializer(serializers.Serializer):
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)
    search = serializers.CharField(max_length=255, required=False, default='')
    property_types = serializers.CharField(
        required=False, default='',
        help_text='Comma separated: Apartment,Villa,Warehouse,Commercial'
    )
    statuses = serializers.CharField(
        required=False, default='',
        help_text='Comma separated: Vacant,Booked,Occupied,Under Maintenance'
    )
    from_date = serializers.DateField(input_formats=["%d-%m-%y"], required=False, allow_null=True, default=None)
    to_date = serializers.DateField(input_formats=["%d-%m-%y"], required=False, allow_null=True, default=None)

    def create(self, validated_data) -> OccupancyReportRequest:
        from_date = validated_data.pop('from_date', None)
        to_date = validated_data.pop('to_date', None)
        if from_date:
            from_date = timezone.make_aware(datetime.combine(from_date, time.min))
        if to_date:
            to_date = timezone.make_aware(datetime.combine(to_date, time.max))

        property_types = validated_data.pop('property_types', '') or ''
        statuses = validated_data.pop('statuses', '') or ''

        return OccupancyReportRequest(
            property_types=[t.strip() for t in property_types.split(',') if t.strip()],
            statuses=[s.strip() for s in statuses.split(',') if s.strip()],
            from_date=from_date,
            to_date=to_date,
            **validated_data
        )
