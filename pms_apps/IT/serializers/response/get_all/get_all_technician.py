from rest_framework import serializers
from pms_apps.IT.serializers.response.get.get_technician import ITTechnicianGetSerializer


class ITTechnicianGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=ITTechnicianGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class ITTechnicianResponseGetAllSerializer(serializers.Serializer):
    data = ITTechnicianGetSerializer()
