from rest_framework import serializers


class CheckOutGetSerializer(serializers.Serializer):
    # A. Check-Out Information
    checkOutId = serializers.IntegerField(read_only=True)
    checkOutCode = serializers.CharField(read_only=True)
    checkOutDate = serializers.DateField(read_only=True, allow_null=True)
    checkOutStatus = serializers.CharField(read_only=True)
    remarksNotes = serializers.CharField(read_only=True, allow_blank=True)
    propertyId = serializers.IntegerField(read_only=True)
    propertyAssignmentId = serializers.IntegerField(read_only=True, allow_null=True)
    checkInId = serializers.IntegerField(read_only=True, allow_null=True)
    tenantId = serializers.IntegerField(read_only=True, allow_null=True)
    assignedEmployeeId = serializers.IntegerField(read_only=True, allow_null=True)

    # B. Tenant Details
    tenantCode = serializers.CharField(read_only=True, allow_null=True)
    tenantName = serializers.CharField(read_only=True, allow_null=True)
    tenantType = serializers.CharField(read_only=True, allow_null=True)
    tenantMobileNumber = serializers.CharField(read_only=True, allow_null=True)
    tenantEmail = serializers.CharField(read_only=True, allow_null=True)
    tenantCivilId = serializers.CharField(read_only=True, allow_null=True)
    tenantPassportNumber = serializers.CharField(read_only=True, allow_null=True)
    tenantNationality = serializers.CharField(read_only=True, allow_null=True)

    # C. Property Details
    propertyType = serializers.CharField(read_only=True, allow_null=True)
    propertyCode = serializers.CharField(read_only=True, allow_null=True)
    buildingName = serializers.CharField(read_only=True, allow_null=True)
    flatUnitNumber = serializers.CharField(read_only=True, allow_null=True)
    floorNumber = serializers.CharField(read_only=True, allow_null=True)
    propertyStatus = serializers.CharField(read_only=True, allow_null=True)

    # D. Rental Details
    monthlyRent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    securityDeposit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    advanceRentReceived = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    firstMonthRentPaid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    paymentMode = serializers.CharField(read_only=True, allow_null=True)
    maintenanceCharges = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)

    # E. Property Inspection
    inspectionRequired = serializers.CharField(read_only=True, allow_null=True)
    inspectionDate = serializers.DateField(read_only=True, allow_null=True)
    technicianType = serializers.CharField(read_only=True, allow_null=True)
    managerApproval = serializers.CharField(read_only=True, allow_null=True)
    issueIdentified = serializers.CharField(read_only=True, allow_blank=True)
    supervisorRemarks = serializers.CharField(read_only=True, allow_blank=True)

    # F. Repair & Damage
    repairRequired = serializers.CharField(read_only=True, allow_null=True)
    quotationAmount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    inventoryAvailable = serializers.CharField(read_only=True, allow_null=True)
    gmApproval = serializers.CharField(read_only=True, allow_null=True)
    landlordConsent = serializers.CharField(read_only=True, allow_null=True)
    financeAlertGenerated = serializers.CharField(read_only=True, allow_null=True)
    rentAdjustmentAmount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)

    # G. Check-Out Utility Meter Readings
    electricityMeterReading = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    waterMeterReading = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    gasMeterReading = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)

    # H. Finance Details
    chargeType = serializers.CharField(read_only=True, allow_null=True)
    totalAmount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    paymentStatus = serializers.CharField(read_only=True, allow_null=True)
    paymentDate = serializers.DateField(read_only=True, allow_null=True)
    transactionId = serializers.CharField(read_only=True, allow_null=True)
    paymentProof = serializers.CharField(read_only=True, allow_null=True)

    # I. Key Return
    keyNumber = serializers.CharField(read_only=True, allow_null=True)
    keyReturn = serializers.CharField(read_only=True, allow_null=True)
    expectedReturnDate = serializers.DateField(read_only=True, allow_null=True)
    confirmationReceived = serializers.CharField(read_only=True, allow_null=True)
    keyReturnDate = serializers.DateField(read_only=True, allow_null=True)
    keyReturnStatus = serializers.CharField(read_only=True)

    # J. Documents Upload
    documents = serializers.ListField(child=serializers.DictField(), read_only=True)

    # K. Comments
    internalComments = serializers.CharField(read_only=True, allow_blank=True)
    tenantRemarks = serializers.CharField(read_only=True, allow_blank=True)
    specialInstructions = serializers.CharField(read_only=True, allow_blank=True)

    # L. System Fields
    createdById = serializers.IntegerField(read_only=True, allow_null=True)
    updatedById = serializers.IntegerField(read_only=True, allow_null=True)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    statusHistory = serializers.CharField(read_only=True, allow_blank=True)
    isActive = serializers.BooleanField(read_only=True)


class CheckOutResponseGetSerializer(serializers.Serializer):
    data = CheckOutGetSerializer()
