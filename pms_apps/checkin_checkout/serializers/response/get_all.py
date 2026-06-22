from rest_framework import serializers


class AssignedEmployeeGetSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True, required=False, allow_null=True)


class CheckInListItemSerializer(serializers.Serializer):
    checkInId = serializers.IntegerField(read_only=True)
    tenantId = serializers.IntegerField(read_only=True, allow_null=True)
    tenantName = serializers.CharField(read_only=True, allow_null=True)
    buildingName = serializers.CharField(read_only=True, allow_null=True)
    flatUnitNumber = serializers.CharField(read_only=True, allow_null=True)
    checkInDate = serializers.DateField(read_only=True, allow_null=True)
    monthlyRent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    managerApproval = serializers.CharField(read_only=True, allow_null=True)
    keyHandoverStatus = serializers.CharField(read_only=True, allow_null=True)
    checkInStatus = serializers.CharField(read_only=True, allow_null=True)
    assignedEmployeeId = serializers.IntegerField(read_only=True, allow_null=True)
    assignedEmployee = AssignedEmployeeGetSerializer(read_only=True, required=False)


class CheckInGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=CheckInListItemSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class CheckInResponseGetAllSerializer(serializers.Serializer):
    data = CheckInGetAllSerializer()
