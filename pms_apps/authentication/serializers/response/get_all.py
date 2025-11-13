from rest_framework import serializers

from pms_apps.common.serializers.response.api_response import APiResponseSerializer
from pms_apps.common.serializers.response.get_all import GetAllGeneralSerializer

class PropertyUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
