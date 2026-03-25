from rest_framework import serializers


class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    email = serializers.EmailField()


class PermissionGetSerializer(serializers.Serializer):
    permissionId = serializers.IntegerField()
    lead = serializers.BooleanField()
    property = serializers.BooleanField()


class MarketingManagerGetSerializer(serializers.Serializer):
    managerId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    department = serializers.CharField(read_only=True)
    campaignsLed = serializers.IntegerField(read_only=True)
    teamSize = serializers.IntegerField(read_only=True)
    profilePicture = serializers.CharField(read_only=True, required=False, allow_blank=True, allow_null=True)
    permission = PermissionGetSerializer(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)


class MarketingManagerResponseGetSerializer(serializers.Serializer):
    data = MarketingManagerGetSerializer()
