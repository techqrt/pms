from rest_framework import serializers


class BuildingUserSerializer(serializers.Serializer):
    userId = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class BuildingGetSerializer(serializers.Serializer):
    buildingId = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    block = serializers.CharField(read_only=True)
    totalFloors = serializers.IntegerField(read_only=True)
    yearOfConstruction = serializers.IntegerField(read_only=True)
    addressLine1 = serializers.CharField(read_only=True)
    addressLine2 = serializers.CharField(read_only=True)
    areaZone = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    state = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True)
    pincode = serializers.CharField(read_only=True)
    googleMapLocation = serializers.CharField(read_only=True)
    internalNotes = serializers.CharField(read_only=True)
    createdBy = BuildingUserSerializer(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    isActive = serializers.BooleanField(read_only=True)


class BuildingResponseGetSerializer(serializers.Serializer):
    data = BuildingGetSerializer(read_only=True)
