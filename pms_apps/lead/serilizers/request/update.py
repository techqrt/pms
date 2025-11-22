from rest_framework import serializers
from pms_apps.lead.serilizers.request.create import UserRequestSerilizer,CountryRequestSerilizer
from pms_apps.lead.dataclasses.request.update import LeadUpdateRequest
from pms_apps.lead.serilizers.request.create import PropertyPermissionRequestSerilizer
from pms_apps.lead.dataclasses.request.update import PropertyPermissionUpdateRequest

class LeadUpdateRequestSerilizer(serializers.Serializer):
    lead_id = serializers.IntegerField()
    lead_assign_to = UserRequestSerilizer(required=False)
    first_name = serializers.CharField(
        max_length = 15,required=False
    )
    last_name = serializers.CharField(
        max_length = 15,required=False
    )
    lead_origin = serializers.CharField(
        max_length = 20,required=False
    )
    address = serializers.CharField(required=False)
    nationality = CountryRequestSerilizer(required=False)
    passport_or_id = serializers.CharField(
        max_length = 50,required=False
    )
    purpose = serializers.CharField(
        max_length = 10,required=False
    )
    created_at = serializers.DateTimeField(
        read_only = True,required=False
    )
    updated_at = serializers.DateTimeField(
        read_only = True,required=False
    )
    permissions = PropertyPermissionRequestSerilizer(required=False)

    def create(self,validated_data) -> LeadUpdateRequest:
        user_data = validated_data.pop('lead_assign_to',{})
        country_data = validated_data.pop('nationality',{})
        permissions_data = validated_data.pop('permissions',{})

        lead_assign_to = user_data.get('user_id',None)
        nationality = country_data.get('country_id',None)
        property_permission = PropertyPermissionUpdateRequest(**permissions_data)
        return LeadUpdateRequest(
            lead_assign_to=lead_assign_to,
            nationality=nationality,
            property_permission = property_permission,
            **validated_data
        )