from rest_framework import serializers

class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    email = serializers.EmailField()

class MaintenanceManagerGetSerializer(serializers.Serializer):
    managerId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    specialization = serializers.CharField(read_only=True)
    teamSize = serializers.IntegerField(read_only=True)
    yearsOfExperience = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)

class MaintenanceManagerResponseGetSerializer(serializers.Serializer):
    data = MaintenanceManagerGetSerializer()