from rest_framework import serializers
from pms_apps.reception.serializers.response.get.get_manager import UserGetSerializer

class ReceptionManagerRefGetSerializer(serializers.Serializer):
    managerId = serializers.IntegerField()

class ReceptionEmployeeGetSerializer(serializers.Serializer):
    employeeId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    shift = serializers.CharField(read_only=True)
    deskNumber = serializers.CharField(read_only=True)
    callsHandled = serializers.IntegerField(read_only=True)
    visitorsLogged = serializers.IntegerField(read_only=True)
    managerRef = ReceptionManagerRefGetSerializer(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)

class ReceptionEmployeeResponseGetSerializer(serializers.Serializer):
    data = ReceptionEmployeeGetSerializer()