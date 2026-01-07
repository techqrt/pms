from rest_framework import serializers
from pms_apps.collection.serializers.response.get.get_manager import UserGetSerializer


class CollectionManagerRefGetSerializer(serializers.Serializer):
    managerId = serializers.IntegerField()


class CollectionEmployeeGetSerializer(serializers.Serializer):
    employeeId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    designation = serializers.CharField(read_only=True)
    region = serializers.CharField(read_only=True)
    collectionsMade = serializers.FloatField(read_only=True)
    overdueAccountsHandled = serializers.IntegerField(read_only=True)
    managerRef = CollectionManagerRefGetSerializer(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)


class CollectionEmployeeResponseGetSerializer(serializers.Serializer):
    data = CollectionEmployeeGetSerializer()
