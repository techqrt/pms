from rest_framework import serializers


class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    email = serializers.EmailField()


class OwnerGetSerializer(serializers.Serializer):
    ownerId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    ownershipType = serializers.CharField(read_only=True)
    propertiesOwned = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)


class OwnerResponseGetSerializer(serializers.Serializer):
    data = OwnerGetSerializer(read_only=True)
