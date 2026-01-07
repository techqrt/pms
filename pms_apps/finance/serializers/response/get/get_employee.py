from rest_framework import serializers
from pms_apps.finance.serializers.response.get.get_manager import UserGetSerializer


class FinanceManagerRefGetSerializer(serializers.Serializer):
    managerId = serializers.IntegerField()


class FinanceEmployeeGetSerializer(serializers.Serializer):
    employeeId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    roleTitle = serializers.CharField(read_only=True)
    invoicesProcessed = serializers.IntegerField(read_only=True)
    paymentsVerified = serializers.IntegerField(read_only=True)
    totalAmountHandled = serializers.FloatField(read_only=True)
    managerRef = FinanceManagerRefGetSerializer(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)


class FinanceEmployeeResponseGetSerializer(serializers.Serializer):
    data = FinanceEmployeeGetSerializer()
