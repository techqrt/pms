from rest_framework import serializers


class AssignedEmployeeGetSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True, required=False, allow_null=True)


class CheckOutListItemSerializer(serializers.Serializer):
    checkOutId = serializers.IntegerField(read_only=True)
    checkOutCode = serializers.CharField(read_only=True, allow_null=True)
    tenantId = serializers.IntegerField(read_only=True, allow_null=True)
    tenantCode = serializers.CharField(read_only=True, allow_null=True)
    tenantName = serializers.CharField(read_only=True, allow_null=True)
    buildingName = serializers.CharField(read_only=True, allow_null=True)
    flatUnitNumber = serializers.CharField(read_only=True, allow_null=True)
    checkOutDate = serializers.DateField(read_only=True, allow_null=True)
    securityDeposit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    managerApproval = serializers.CharField(read_only=True, allow_null=True)
    keyReturnStatus = serializers.CharField(read_only=True, allow_null=True)
    paymentStatus = serializers.CharField(read_only=True, allow_null=True)
    checkOutStatus = serializers.CharField(read_only=True, allow_null=True)
    requestFrom = serializers.CharField(read_only=True, allow_null=True)
    assignedEmployeeId = serializers.IntegerField(read_only=True, allow_null=True)
    assignedEmployee = AssignedEmployeeGetSerializer(read_only=True, required=False)


class CheckOutGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=CheckOutListItemSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class CheckOutResponseGetAllSerializer(serializers.Serializer):
    data = CheckOutGetAllSerializer()
