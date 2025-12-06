from rest_framework import serializers
from pms_apps.marketing.serializers.response.get.get_employee import MarketingEmployeeGetSerializer

class MarketingEmployeeGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=MarketingEmployeeGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class MarketingEmployeeResponseGetAllSerializer(serializers.Serializer):
    data = MarketingEmployeeGetAllSerializer()
