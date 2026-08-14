from datetime import datetime, time

from django.utils import timezone
from rest_framework import serializers

from pms.config import Configurations
from pms_apps.checkin_checkout.dataclasses.requests.get_all_check_in import CheckInGetAllRequest


class CheckInGetAllSerializer(serializers.Serializer):
    values = serializers.CharField(max_length=100, required=False, default='')
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)
    sort_by = serializers.CharField(max_length=100, required=False, default='')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    search_key = serializers.CharField(max_length=100, required=False, default='')
    status = serializers.CharField(
        required=False, default='',
        help_text='Comma separated check_in_status values: Pending,In Progress,Key Pending,Active,Completed,Cancelled'
    )
    building = serializers.CharField(max_length=150, required=False, default='')
    assigned_employee_id = serializers.CharField(required=False, default='', help_text='Comma separated employee IDs')
    manager_approval = serializers.CharField(
        required=False, default='', help_text='Comma separated: Pending,Approved,Rejected'
    )
    key_handover_status = serializers.CharField(
        required=False, default='', help_text='Comma separated: Pending,Booked,Handed Over,Returned'
    )
    from_date = serializers.DateField(input_formats=["%d-%m-%y"], required=False, allow_null=True, default=None)
    to_date = serializers.DateField(input_formats=["%d-%m-%y"], required=False, allow_null=True, default=None)

    def create(self, validated_data) -> CheckInGetAllRequest:
        from_date = validated_data.pop('from_date', None)
        to_date = validated_data.pop('to_date', None)
        if from_date:
            from_date = timezone.make_aware(datetime.combine(from_date, time.min))
        if to_date:
            to_date = timezone.make_aware(datetime.combine(to_date, time.max))

        status_csv = validated_data.pop('status', '') or ''
        assigned_employee_id_csv = validated_data.pop('assigned_employee_id', '') or ''
        manager_approval_csv = validated_data.pop('manager_approval', '') or ''
        key_handover_status_csv = validated_data.pop('key_handover_status', '') or ''

        return CheckInGetAllRequest(
            status=[s.strip() for s in status_csv.split(',') if s.strip()],
            assigned_employee_id=[s.strip() for s in assigned_employee_id_csv.split(',') if s.strip()],
            manager_approval=[s.strip() for s in manager_approval_csv.split(',') if s.strip()],
            key_handover_status=[s.strip() for s in key_handover_status_csv.split(',') if s.strip()],
            from_date=from_date,
            to_date=to_date,
            **validated_data
        )
