from rest_framework import serializers
from pms_apps.property.serializers.response.building_get import BuildingGetSerializer


class BuildingGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=BuildingGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class BuildingResponseGetAllSerializer(serializers.Serializer):
    data = BuildingGetAllSerializer()
