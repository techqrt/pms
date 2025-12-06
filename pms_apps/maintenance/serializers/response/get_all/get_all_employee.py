from rest_framework import serializers
from pms_apps.maintenance.serializers.response.get.get_employee import MaintenanceEmployeeGetSerializer


class MaintenanceEmployeeGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=MaintenanceEmployeeGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class MaintenanceEmployeeResponseGetAllSerializer(serializers.Serializer):
    data = MaintenanceEmployeeGetSerializer()
