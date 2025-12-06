from rest_framework import serializers
from pms_apps.marketing.serializers.response.get.get_manager import MarketingManagerGetSerializer


class MarketingManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=MarketingManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class MarketingManagerResponseGetAllSerializer(serializers.Serializer):
    data = MarketingManagerGetAllSerializer()
