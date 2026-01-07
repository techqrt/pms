from rest_framework import serializers


class CityResponseGetSerializer(serializers.Serializer):
    cityId = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    countryName = serializers.CharField(read_only=True)