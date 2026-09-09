from rest_framework import serializers

from pms.config import Configurations
from pms_apps.common.dataclasses.search import Search


class SearchSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=100, required=False,default='')
    page_num = serializers.IntegerField(
        default=1, min_value=1, error_messages={'min_value': 'Must be 1 or greater.'}
    )
    limit = serializers.IntegerField(
        default=Configurations.pagination_count, min_value=1,
        error_messages={'min_value': 'Must be greater than 0.'}
    )

    def create(self, validated_data) -> Search:
        return Search(**validated_data)
