from rest_framework import serializers


class TenantGetSerializer(serializers.Serializer):
    tenantId = serializers.IntegerField(read_only=True)
    firstName = serializers.CharField(read_only=True)
    lastName = serializers.CharField(read_only=True)
    phoneNumber = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


class AssignedByGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField(read_only=True)
    phoneNumber = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


class PropertyGetSerializer(serializers.Serializer):
    propertyId = serializers.IntegerField(read_only=True)
    block = serializers.CharField(read_only=True)
    buildingDetails = serializers.CharField(read_only=True)
    floor = serializers.CharField(read_only=True)
    flatNumber = serializers.IntegerField(read_only=True)


class AssignmentGetSerializer(serializers.Serializer):
    assignmentId = serializers.IntegerField(read_only=True)
    property = PropertyGetSerializer(read_only=True)
    tenant = TenantGetSerializer(read_only=True)
    assignedBy = AssignedByGetSerializer(read_only=True)
    
    # Assignment Status
    assignmentStatus = serializers.CharField(read_only=True)
    companyName = serializers.CharField(read_only=True, allow_null=True)
    
    # Rental Details
    rentalStartDate = serializers.DateField(read_only=True, allow_null=True)
    rentalEndDate = serializers.DateField(read_only=True, allow_null=True)
    agreementDurationMonths = serializers.IntegerField(read_only=True, allow_null=True)
    maintenanceCharges = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    advanceRentPaid = serializers.BooleanField(read_only=True)
    paymentMode = serializers.CharField(read_only=True, allow_null=True)
    
    # Agreement Details
    agreementType = serializers.CharField(read_only=True, allow_null=True)
    agreementStatus = serializers.CharField(read_only=True)
    keyAvailableInOffice = serializers.BooleanField(read_only=True)
    keyCode = serializers.CharField(read_only=True, allow_null=True)
    keyHandoverDate = serializers.DateField(read_only=True, allow_null=True)
    keyHandoverStatus = serializers.CharField(read_only=True)
    
    # Utility Details
    electricityMeterNumber = serializers.CharField(read_only=True, allow_null=True)
    electricityMeterReadingStart = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    waterMeterReadingStart = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    gasMeterReadingStart = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    
    # Financial Approval
    financeApprovalStatus = serializers.CharField(read_only=True)
    rentEntryCreated = serializers.BooleanField(read_only=True)
    invoiceGenerated = serializers.BooleanField(read_only=True)
    
    # Maintenance Check
    maintenanceRequired = serializers.BooleanField(read_only=True)
    maintenanceTicketId = serializers.CharField(read_only=True, allow_null=True)
    maintenanceStatus = serializers.CharField(read_only=True)
    
    # Internal Tracking
    internalNotes = serializers.CharField(read_only=True)
    tenantSpecialRequirements = serializers.CharField(read_only=True)
    
    # Timestamps
    assignedOn = serializers.DateTimeField(read_only=True)
    unassignedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)


class PropertyAssignmentResponseGetSerializer(serializers.Serializer):
    data = AssignmentGetSerializer(read_only=True)
