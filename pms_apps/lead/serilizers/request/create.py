from rest_framework import serializers
from pms_apps.lead.dataclasses.request.create import LeadCreateRequest,PropertyPermissionCreateRequest

class PropertyPermissionRequestSerilizer(serializers.Serializer):
    property = serializers.BooleanField(required = False)

class CountryRequestSerilizer(serializers.Serializer):
    country_id = serializers.IntegerField()

class UserRequestSerilizer(serializers.Serializer):
    user_id = serializers.IntegerField()


class LeadCreateRequestSerilizer(serializers.Serializer):
    lead_id = serializers.IntegerField(
        read_only = True
    )
    lead_assign_to = UserRequestSerilizer()
    first_name = serializers.CharField(
        max_length = 15
    )
    last_name = serializers.CharField(
        max_length = 15
    )
    lead_origin = serializers.CharField(
        max_length = 20
    )
    address = serializers.CharField()
    nationality = CountryRequestSerilizer()
    passport_or_id = serializers.CharField(
        max_length = 50
    )
    purpose = serializers.CharField(
        max_length = 10
    )
    created_at = serializers.DateTimeField(
        read_only = True
    )
    updated_at = serializers.DateTimeField(
        read_only = True
    )
    permissions = PropertyPermissionRequestSerilizer()

    def create(self,validated_data) -> LeadCreateRequest:
        print(f'Validated Data : {validated_data}')
        user_data = validated_data.pop('lead_assign_to')
        country_data = validated_data.pop('nationality')
        permission_data = validated_data.pop('permissions')

        lead_assign_to = user_data['user_id']
        nationality = country_data['country_id']
        property_permission = PropertyPermissionCreateRequest(**permission_data)

        return LeadCreateRequest(
            lead_assign_to=lead_assign_to,
            nationality=nationality,
            property_permission = property_permission,
            **validated_data
        )
    


        

