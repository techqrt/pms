from rest_framework import serializers

from pms.config import Configurations
from pms_apps.common.dataclasses.get_all import GetAll


class GetAllSerializer(serializers.Serializer):
    values = serializers.CharField(max_length=100, required=False, default='')
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)
    sort_by = serializers.CharField(max_length=100, required=False, default='')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter_key = serializers.CharField(max_length=100, required=False, default='')
    filter_value = serializers.CharField(max_length=100, required=False, default='')
    search_key = serializers.CharField(max_length=100, required=False, default='')

    def create(self, validated_data) -> GetAll:
        return GetAll(**validated_data)
