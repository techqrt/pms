from rest_framework import serializers


class CheckInDocumentGetSerializer(serializers.Serializer):
    documentId = serializers.IntegerField(read_only=True)
    documentType = serializers.CharField(read_only=True, allow_null=True)
    file = serializers.CharField(read_only=True, allow_null=True)


class CheckInActivityTimelineSerializer(serializers.Serializer):
    propertyCreatedDate = serializers.DateField(read_only=True, allow_null=True)
    listedForRentDate = serializers.DateField(read_only=True, allow_null=True)
    tenantAssignedDate = serializers.DateField(read_only=True, allow_null=True)
    assignedToEmployeeDate = serializers.DateField(read_only=True, allow_null=True)
    propertyOccupiedDate = serializers.DateField(read_only=True, allow_null=True)


class CheckInLandlordDetailsSerializer(serializers.Serializer):
    landlordId = serializers.IntegerField(read_only=True, allow_null=True)
    name = serializers.CharField(read_only=True, allow_null=True)
    mobileNumber = serializers.CharField(read_only=True, allow_null=True)
    email = serializers.CharField(read_only=True, allow_null=True)
    address = serializers.CharField(read_only=True, allow_null=True)


class CheckInOverviewSerializer(serializers.Serializer):
    propertyInformation = serializers.DictField(read_only=True, allow_null=True)
    rentAndCharges = serializers.DictField(read_only=True, allow_null=True)
    activityTimeline = CheckInActivityTimelineSerializer(read_only=True)
    landlordDetails = CheckInLandlordDetailsSerializer(read_only=True, allow_null=True)
    propertyFeatures = serializers.DictField(read_only=True, allow_null=True)
    tenantDocuments = CheckInDocumentGetSerializer(many=True, read_only=True)
    photos = serializers.ListField(child=serializers.CharField(), read_only=True)


class CheckInTenantDetailsSerializer(serializers.Serializer):
    personalDetails = serializers.DictField(read_only=True, allow_null=True)
    contactDetails = serializers.DictField(read_only=True, allow_null=True)
    identificationDetails = serializers.DictField(read_only=True, allow_null=True)
    professionalDetails = serializers.DictField(read_only=True, allow_null=True)
    occupancyDetails = serializers.DictField(read_only=True, allow_null=True)


class CheckInPropertyDetailsTabSerializer(serializers.Serializer):
    propertyName = serializers.CharField(read_only=True, allow_null=True)
    address = serializers.CharField(read_only=True, allow_null=True, allow_blank=True)
    monthlyRent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    photos = serializers.ListField(child=serializers.CharField(), read_only=True)
    basicInformation = serializers.DictField(read_only=True, allow_null=True)
    configurationAndArea = serializers.DictField(read_only=True, allow_null=True)
    rentalAndFinancialDetails = serializers.DictField(read_only=True, allow_null=True)
    ownership = serializers.DictField(read_only=True, allow_null=True)
    amenitiesAndFacilities = serializers.ListField(child=serializers.CharField(), read_only=True)
    rentalDetails = serializers.DictField(read_only=True, allow_null=True)
    agreementDetails = serializers.DictField(read_only=True, allow_null=True)
    residentialAddress = serializers.DictField(read_only=True, allow_null=True)
    systemInformation = serializers.DictField(read_only=True, allow_null=True)


class CheckInInspectionTabSerializer(serializers.Serializer):
    summary = serializers.DictField(read_only=True, allow_null=True)
    inspectionsList = serializers.ListField(child=serializers.DictField(), read_only=True)
    inspectionOverview = serializers.DictField(read_only=True, allow_null=True)
    topIssuesCategories = serializers.ListField(child=serializers.DictField(), read_only=True)
    inspectionPhotos = serializers.ListField(child=serializers.CharField(), read_only=True)
    recentIssues = serializers.ListField(child=serializers.DictField(), read_only=True)


class CheckInRepairApprovalTabSerializer(serializers.Serializer):
    summary = serializers.DictField(read_only=True, allow_null=True)
    issueList = serializers.ListField(child=serializers.DictField(), read_only=True)
    approvalSummary = serializers.DictField(read_only=True, allow_null=True)
    pendingRepairs = serializers.ListField(child=serializers.DictField(), read_only=True)
    repairedPhotos = serializers.ListField(child=serializers.CharField(), read_only=True)
    recentResolvedIssues = serializers.ListField(child=serializers.DictField(), read_only=True)


class CheckInUtilityReadingsTabSerializer(serializers.Serializer):
    summary = serializers.DictField(read_only=True, allow_null=True)
    readingsList = serializers.ListField(child=serializers.DictField(), read_only=True)
    utilitiesOverview = serializers.DictField(read_only=True, allow_null=True)
    readingOverview = serializers.ListField(child=serializers.DictField(), read_only=True)


class CheckInAgreementTabSerializer(serializers.Serializer):
    agreementDetails = serializers.DictField(read_only=True, allow_null=True)
    agreementTimeline = serializers.ListField(child=serializers.DictField(), read_only=True)
    rentAndPaymentSummary = serializers.DictField(read_only=True, allow_null=True)
    agreementDocuments = serializers.ListField(child=serializers.DictField(), read_only=True)
    agreementNotes = serializers.CharField(read_only=True, allow_null=True, allow_blank=True)


class CheckInKeyHandoverTabSerializer(serializers.Serializer):
    keyHandoverInformation = serializers.DictField(read_only=True, allow_null=True)
    keyHandoverTimeline = serializers.ListField(child=serializers.DictField(), read_only=True)
    keyDetails = serializers.ListField(child=serializers.DictField(), read_only=True)
    attachments = serializers.ListField(child=serializers.DictField(), read_only=True)
    tenantConfirmation = serializers.CharField(read_only=True, allow_null=True, allow_blank=True)
    relatedInformation = serializers.DictField(read_only=True, allow_null=True)


class CheckInDocumentsTabSerializer(serializers.Serializer):
    summary = serializers.DictField(read_only=True, allow_null=True)
    allDocuments = serializers.ListField(child=serializers.DictField(), read_only=True)
    expiringSoon = serializers.ListField(child=serializers.DictField(), read_only=True)
    missingDocuments = serializers.ListField(child=serializers.DictField(), read_only=True)
    notes = serializers.CharField(read_only=True, allow_null=True, allow_blank=True)


class CheckInGetSerializer(serializers.Serializer):
    checkInId = serializers.IntegerField(read_only=True)
    checkInCode = serializers.CharField(read_only=True)
    checkInDate = serializers.DateField(read_only=True, allow_null=True)
    checkInStatus = serializers.CharField(read_only=True)
    remarksNotes = serializers.CharField(read_only=True, allow_blank=True)
    propertyId = serializers.IntegerField(read_only=True)
    propertyAssignmentId = serializers.IntegerField(read_only=True, allow_null=True)
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
    tenantAddress = serializers.CharField(read_only=True, allow_blank=True)
    dateOfBirth = serializers.DateField(read_only=True, allow_null=True)
    gender = serializers.CharField(read_only=True, allow_null=True)
    maritalStatus = serializers.CharField(read_only=True, allow_null=True)
    alternateMobileNumber = serializers.CharField(read_only=True, allow_null=True)
    emergencyContactName = serializers.CharField(read_only=True, allow_null=True)
    emergencyContactNumber = serializers.CharField(read_only=True, allow_null=True)
    profession = serializers.CharField(read_only=True, allow_null=True)
    companyName = serializers.CharField(read_only=True, allow_null=True)
    moveInReason = serializers.CharField(read_only=True, allow_null=True)
    numberOfOccupants = serializers.IntegerField(read_only=True, allow_null=True)

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
    inspectionPriority = serializers.CharField(read_only=True, allow_null=True)
    inspectionType = serializers.CharField(read_only=True, allow_null=True)
    inspectionDuration = serializers.CharField(read_only=True, allow_null=True)
    nextInspectionDue = serializers.DateField(read_only=True, allow_null=True)

    # F. Repair & Approval
    repairRequired = serializers.CharField(read_only=True, allow_null=True)
    quotationAmount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    inventoryAvailable = serializers.CharField(read_only=True, allow_null=True)
    gmApproval = serializers.CharField(read_only=True, allow_null=True)
    landlordConsent = serializers.CharField(read_only=True, allow_null=True)
    financeAlertGenerated = serializers.CharField(read_only=True, allow_null=True)
    rentAdjustmentAmount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    repairPriority = serializers.CharField(read_only=True, allow_null=True)
    recommendedById = serializers.IntegerField(read_only=True, allow_null=True)
    approvedById = serializers.IntegerField(read_only=True, allow_null=True)
    approvedOn = serializers.DateField(read_only=True, allow_null=True)
    inspectorComments = serializers.CharField(read_only=True, allow_blank=True)

    # G. Utility Meter Readings
    electricityMeterReading = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    waterMeterReading = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    gasMeterReading = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    utilityAdjustmentAmount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)

    # H. Agreement Details
    agreementType = serializers.CharField(read_only=True, allow_null=True)
    agreementStatus = serializers.CharField(read_only=True)
    agreementStartDate = serializers.DateField(read_only=True, allow_null=True)
    agreementEndDate = serializers.DateField(read_only=True, allow_null=True)
    agreementDocument = serializers.CharField(read_only=True, allow_null=True)
    agreementTemplate = serializers.CharField(read_only=True, allow_null=True)
    agreementNumber = serializers.CharField(read_only=True, allow_null=True)
    generatedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    generatedById = serializers.IntegerField(read_only=True, allow_null=True)
    submittedToTenantOn = serializers.DateTimeField(read_only=True, allow_null=True)
    tenantSignedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    managerSignedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    signedById = serializers.IntegerField(read_only=True, allow_null=True)
    renewalReminderDate = serializers.DateField(read_only=True, allow_null=True)
    autoReminderEnabled = serializers.BooleanField(read_only=True, allow_null=True)
    agreementNotes = serializers.CharField(read_only=True, allow_blank=True)

    # I. Key Handover
    keyNumber = serializers.CharField(read_only=True, allow_null=True)
    keyType = serializers.CharField(read_only=True, allow_null=True)
    keyAvailable = serializers.CharField(read_only=True, allow_null=True)
    keyBookingDate = serializers.DateField(read_only=True, allow_null=True)
    confirmationReceived = serializers.CharField(read_only=True, allow_null=True)
    keyDeliveryDate = serializers.DateField(read_only=True, allow_null=True)
    keyHandoverStatus = serializers.CharField(read_only=True)
    expectedHandoverDate = serializers.DateTimeField(read_only=True, allow_null=True)
    handoverNotes = serializers.CharField(read_only=True, allow_blank=True)
    tenantConfirmationNotes = serializers.CharField(read_only=True, allow_blank=True)
    keyBookedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    keyBookedById = serializers.IntegerField(read_only=True, allow_null=True)
    keyPreparedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    keyNotifiedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    handoverCompletedOn = serializers.DateTimeField(read_only=True, allow_null=True)
    handedOverById = serializers.IntegerField(read_only=True, allow_null=True)

    # J. Documents Upload
    documents = CheckInDocumentGetSerializer(many=True, read_only=True)

    # Overview Tab (nested)
    overview = CheckInOverviewSerializer(read_only=True)

    # Tenant Details Tab (nested)
    tenantDetails = CheckInTenantDetailsSerializer(read_only=True)

    # Property Details Tab (nested)
    propertyDetails = CheckInPropertyDetailsTabSerializer(read_only=True)

    # Inspection Tab (nested)
    inspection = CheckInInspectionTabSerializer(read_only=True)

    # Repair & Approval Tab (nested)
    repairApproval = CheckInRepairApprovalTabSerializer(read_only=True)

    # Utility Readings Tab (nested)
    utilityReadings = CheckInUtilityReadingsTabSerializer(read_only=True)

    # Agreement Tab (nested)
    agreement = CheckInAgreementTabSerializer(read_only=True)

    # Key Handover Tab (nested)
    keyHandover = CheckInKeyHandoverTabSerializer(read_only=True)

    # Documents Tab (nested)
    documentsTab = CheckInDocumentsTabSerializer(read_only=True)

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


class CheckInResponseGetSerializer(serializers.Serializer):
    data = CheckInGetSerializer(read_only=True)
