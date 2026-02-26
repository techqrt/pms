from rest_framework import serializers
from pms_apps.IT.serializers.response.get.get_manager import ITManagerGetSerializer


class ITManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=ITManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class ITManagerResponseGetAllSerializer(serializers.Serializer):
    data = ITManagerGetAllSerializer()
