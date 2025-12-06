from rest_framework import serializers
from pms_apps.maintenance.serializers.response.get.get_manager import MaintenanceManagerGetSerializer


class MaintenanceManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=MaintenanceManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class MaintenanceManagerResponseGetAllSerializer(serializers.Serializer):
    data = MaintenanceManagerGetAllSerializer()
