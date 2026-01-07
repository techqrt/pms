from rest_framework import serializers
from pms_apps.helper_apis.serilizers.country.response.get import CountryResponseGetSerializer

class CountryGetAllSerilizers(serializers.Serializer):
    data = serializers.ListField(child=CountryResponseGetSerializer())
    presentPage = serializers.IntegerField(read_only=True)
    totalPage = serializers.IntegerField(read_only=True)

class CountryResponseGetAllSerilizers(serializers.Serializer):
    data = CountryGetAllSerilizers(read_only = True)