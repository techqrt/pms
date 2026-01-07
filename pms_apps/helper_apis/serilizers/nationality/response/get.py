from rest_framework import serializers

class NationalityResponseGetSerializers(serializers.Serializer):
    nationalityId = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)