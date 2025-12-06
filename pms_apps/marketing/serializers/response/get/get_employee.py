from rest_framework import serializers
from pms_apps.marketing.serializers.response.get.get_manager import UserGetSerializer
from pms_apps.marketing.serializers.response.get.get_manager import PermissionGetSerializer


class MarketingManagerRefGetSerializer(serializers.Serializer):
    managerId = serializers.IntegerField()


class MarketingEmployeeGetSerializer(serializers.Serializer):
    employeeId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    designation = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)
    campaignsAssigned = serializers.IntegerField(read_only=True)
    leadsGenerated = serializers.IntegerField(read_only=True)
    managerRef = MarketingManagerRefGetSerializer(required=False)
    permission = PermissionGetSerializer(required=False, read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)


class MarketingEmployeeResponseGetSerializer(serializers.Serializer):
    data = MarketingEmployeeGetSerializer()
