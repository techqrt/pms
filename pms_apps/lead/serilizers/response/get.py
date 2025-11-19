from rest_framework import serializers

class LeadPermissionsGetSeriazlier(serializers.Serializer):
    property =  serializers.BooleanField()

class CountryGetSerializer(serializers.Serializer):
    name = serializers.CharField()

class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()

class LeadGetSerializer(serializers.Serializer):
    leadId = serializers.IntegerField(read_only = True)
    leadAssignTo = UserGetSerializer(read_only = True)
    firstName = serializers.CharField(read_only = True)
    lastName = serializers.CharField(read_only = True)
    leadOrigin = serializers.CharField(read_only = True)
    address = serializers.CharField(read_only = True)
    nationality = CountryGetSerializer(read_only = True)
    passportOrId = serializers.CharField(read_only = True)
    purpose = serializers.CharField(read_only = True)
    createdAt = serializers.DateTimeField(read_only = True)
    updatedAt = serializers.DateTimeField(read_only = True)
    isActive = serializers.BooleanField(read_only = True)
    permissions = LeadPermissionsGetSeriazlier(read_only = True)

class LeadResponseGetSerializer(serializers.Serializer):
    data = LeadGetSerializer()