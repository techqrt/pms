from rest_framework import serializers


class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField(read_only=True)
    phoneNumber = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


class PropertyGetSerializer(serializers.Serializer):
    block = serializers.CharField(read_only=True)
    propertyId = serializers.IntegerField(read_only=True)
    buildingId = serializers.IntegerField(read_only=True, required=False)
    buildingName = serializers.CharField(read_only=True, required=False)
    buildingDetails = serializers.CharField(read_only=True)
    floor = serializers.CharField(read_only=True)
    flatNumber = serializers.IntegerField(read_only=True)
    dimensionLengthFt = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    dimensionBreadthFt = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    dimensionAreaSqft = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    rentalType = serializers.CharField(read_only=True)
    rentalFor = serializers.CharField(read_only=True)
    advanceAmountRent = serializers.IntegerField(read_only=True)
    expectedRent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    agreementId = serializers.IntegerField(read_only=True)
    photos = serializers.ListField(child=serializers.URLField(), read_only=True)
    videos = serializers.ListField(child=serializers.URLField(), read_only=True)
    createdBy = UserGetSerializer(read_only=True)
    assignedTo = UserGetSerializer(many=True, read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    isActive = serializers.BooleanField(read_only=True)

    # Nested details
    propertyDetails = serializers.DictField(read_only=True)
    commercialData = serializers.DictField(read_only=True)
    flatData = serializers.DictField(read_only=True)
    villaData = serializers.DictField(read_only=True)


class PropertyResponseGetSerializer(serializers.Serializer):
    data = PropertyGetSerializer(read_only=True)
