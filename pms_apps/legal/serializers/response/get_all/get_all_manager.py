from rest_framework import serializers
from pms_apps.legal.serializers.response.get.get_manager import LegalManagerGetSerializer


class LegalManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=LegalManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class LegalManagerResponseGetAllSerializer(serializers.Serializer):
    data = LegalManagerGetAllSerializer()
