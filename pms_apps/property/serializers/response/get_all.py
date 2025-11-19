from rest_framework import serializers
from pms_apps.property.serializers.response.get import PropertyResponseGetSerializer

class PropertyGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=PropertyResponseGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()

class PropertyResponseGetAllSerializer(serializers.Serializer):
    data = PropertyGetAllSerializer()