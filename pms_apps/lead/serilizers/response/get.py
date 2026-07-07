from rest_framework import serializers
from pms_apps.property.image_utils import ImageUtils

class LeadPermissionsGetSeriazlier(serializers.Serializer):
    property =  serializers.BooleanField()

class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()

class LeadGetSerializer(serializers.Serializer):
    leadId = serializers.IntegerField(read_only = True)
    leadAssignTo = UserGetSerializer(read_only = True)
    firstName = serializers.CharField(read_only = True)
    lastName = serializers.CharField(read_only = True)
    leadOrigin = serializers.CharField(read_only = True)
    address = serializers.CharField(read_only = True)
    country = serializers.CharField(read_only = True)
    city = serializers.CharField(read_only=True)
    nationality = serializers.CharField(read_only=True)
    passportOrId = serializers.CharField(read_only = True)
    purpose = serializers.CharField(read_only = True)
    poBox = serializers.CharField(read_only = True, required=False)
    feedback = serializers.CharField(read_only = True, required=False)
    leadCategory = serializers.CharField(read_only = True, required=False)
    createdAt = serializers.DateTimeField(read_only = True)
    updatedAt = serializers.DateTimeField(read_only = True)
    isActive = serializers.BooleanField(read_only = True)
    phoneNumber = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True, required=False, allow_null=True)
    tenantCode = serializers.CharField(read_only=True, required=False, allow_null=True)
    tenantType = serializers.CharField(read_only=True, required=False, allow_null=True)
    dateOfBirth = serializers.DateField(read_only=True, required=False, allow_null=True)
    gender = serializers.CharField(read_only=True, required=False, allow_null=True)
    maritalStatus = serializers.CharField(read_only=True, required=False, allow_null=True)
    alternateMobileNumber = serializers.CharField(read_only=True, required=False, allow_null=True)
    emergencyContactName = serializers.CharField(read_only=True, required=False, allow_null=True)
    emergencyContactNumber = serializers.CharField(read_only=True, required=False, allow_null=True)
    profession = serializers.CharField(read_only=True, required=False, allow_null=True)
    companyName = serializers.CharField(read_only=True, required=False, allow_null=True)
    profileImage = serializers.SerializerMethodField(read_only=True)
    permissions = LeadPermissionsGetSeriazlier(read_only = True)

    def get_profileImage(self, obj):
        """Convert profile_image file path to URL"""
        try:
            profile_image = obj.get('profile_image') if isinstance(obj, dict) else getattr(obj, 'profile_image', None)
            
            if not profile_image:
                return None
            
            # If it's already a full URL, return as-is
            profile_image_str = str(profile_image)
            if profile_image_str.startswith('http://') or profile_image_str.startswith('https://'):
                return profile_image_str
            
            # Convert file path to URL
            if profile_image_str:
                return ImageUtils.get_photo_url(profile_image_str)
            
            return None
        except Exception:
            # If any error occurs during URL conversion, return None safely
            return None

class LeadResponseGetSerializer(serializers.Serializer):
    data = LeadGetSerializer()