from rest_framework import serializers
from pms_apps.reception.serializers.response.get.get_employee import ReceptionEmployeeGetSerializer


class ReceptionEmployeeGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=ReceptionEmployeeGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class ReceptionEmployeeResponseGetAllSerializer(serializers.Serializer):
    data = ReceptionEmployeeGetAllSerializer()