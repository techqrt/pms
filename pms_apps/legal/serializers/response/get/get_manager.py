from rest_framework import serializers

class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    email = serializers.EmailField()

class LegalManagerGetSerializer(serializers.Serializer):
    managerId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    department = serializers.CharField(read_only=True)
    totalCasesHandled = serializers.IntegerField(read_only=True)
    openCases = serializers.IntegerField(read_only=True)
    closedCases = serializers.IntegerField(read_only=True)
    teamSize = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)

class LegalManagerResponseGetSerializer(serializers.Serializer):
    data = LegalManagerGetSerializer()