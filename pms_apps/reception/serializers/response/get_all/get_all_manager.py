from rest_framework import serializers
from pms_apps.reception.serializers.response.get.get_manager import ReceptionManagerGetSerializer


class ReceptionManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=ReceptionManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class ReceptionManagerResponseGetAllSerializer(serializers.Serializer):
    data = ReceptionManagerGetAllSerializer()