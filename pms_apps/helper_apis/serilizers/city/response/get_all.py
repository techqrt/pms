from rest_framework import serializers
from pms_apps.helper_apis.serilizers.city.response.get import CityResponseGetSerializer

class CityGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=CityResponseGetSerializer())
    presentPage = serializers.IntegerField(read_only=True)
    totalPage = serializers.IntegerField(read_only=True)

class CityResponseGetAllSerializer(serializers.Serializer):
    data = CityGetAllSerializer(read_only=True)