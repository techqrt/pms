from rest_framework import serializers
from pms_apps.general_manager.serializers.response.get import GeneralManagerGetSerializer


class GeneralManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=GeneralManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class GeneralManagerResponseGetAllSerializer(serializers.Serializer):
    data = GeneralManagerGetAllSerializer()