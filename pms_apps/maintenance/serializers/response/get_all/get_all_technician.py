from rest_framework import serializers
from pms_apps.maintenance.serializers.response.get.get_technician import MaintenanceTechnicianGetSerializer


class MaintenanceTechnicianGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=MaintenanceTechnicianGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class MaintenanceTechnicianResponseGetAllSerializer(serializers.Serializer):
    data = MaintenanceTechnicianGetSerializer()
