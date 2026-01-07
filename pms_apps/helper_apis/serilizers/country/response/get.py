from rest_framework import serializers

class CountryResponseGetSerializer(serializers.Serializer):
    countryId = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    