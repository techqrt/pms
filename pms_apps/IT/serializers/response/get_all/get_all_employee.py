from rest_framework import serializers
from pms_apps.IT.serializers.response.get.get_employee import ITEmployeeGetSerializer


class ITEmployeeGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=ITEmployeeGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class ITEmployeeResponseGetAllSerializer(serializers.Serializer):
    data = ITEmployeeGetSerializer()
