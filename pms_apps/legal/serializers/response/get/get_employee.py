from rest_framework import serializers
from pms_apps.legal.serializers.response.get.get_manager import UserGetSerializer


class LegalManagerRefGetSerializer(serializers.Serializer):
    managerId = serializers.IntegerField()


class LegalEmployeeGetSerializer(serializers.Serializer):
    employeeId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    designation = serializers.CharField(read_only=True)
    activeCases = serializers.IntegerField(read_only=True)
    caseSpecialization = serializers.IntegerField(read_only=True)
    managerRef = LegalManagerRefGetSerializer(required=False)
    createdAt = serializers.DateTimeField(read_only=True)


class LegalEmployeeResponseGetSerializer(serializers.Serializer):
    data = LegalEmployeeGetSerializer()
