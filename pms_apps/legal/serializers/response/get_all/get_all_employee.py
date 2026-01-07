from rest_framework import serializers
from pms_apps.legal.serializers.response.get.get_employee import LegalEmployeeGetSerializer


class LegalEmployeeGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=LegalEmployeeGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class LegalEmployeeResponseGetAllSerializer(serializers.Serializer):
    data = LegalEmployeeGetSerializer()
