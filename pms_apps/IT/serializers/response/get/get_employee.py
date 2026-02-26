from rest_framework import serializers
from pms_apps.IT.serializers.response.get.get_manager import UserGetSerializer


class ITManagerRefGetSerializer(serializers.Serializer):
    managerId = serializers.IntegerField()


class ITEmployeeGetSerializer(serializers.Serializer):
    employeeId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    roleTitle = serializers.CharField(read_only=True)
    ticketsResolved = serializers.IntegerField(read_only=True)
    projectsAssigned = serializers.IntegerField(read_only=True)
    specialization = serializers.CharField(read_only=True)
    managerRef = ITManagerRefGetSerializer(required=False)
    createdAt = serializers.DateTimeField(read_only=True)


class ITEmployeeResponseGetSerializer(serializers.Serializer):
    data = ITEmployeeGetSerializer()
