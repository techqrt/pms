from rest_framework import serializers
from pms_apps.common.dataclasses.request.permission import Permissions
from pms_apps.lead.dataclasses.request.create import LeadCreateRequest
from pms_apps.property.serializers.fields import Base64ImageField

class PropertyPermissionRequestSerilizer(serializers.Serializer):
    property = serializers.BooleanField(required = False)

class CityRequestSerializer(serializers.Serializer):
    city_id = serializers.IntegerField()

class CountryRequestSerializer(serializers.Serializer):
    country_id = serializers.IntegerField()

class NationalityRequestSerializer(serializers.Serializer):
    nationality_id = serializers.IntegerField()

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
    phone_number = serializers.CharField(
        max_length = 20
    )
    lead_origin = serializers.CharField(
        max_length = 20
    )
    address = serializers.CharField()
    country = CountryRequestSerializer()
    city = CityRequestSerializer()
    nationality = NationalityRequestSerializer()
    passport_or_id = serializers.CharField(
        max_length = 50
    )
    purpose = serializers.CharField(
        max_length = 10
    )
    po_box = serializers.CharField(
        max_length = 20,
        required = False,
        allow_null = True
    )
    feedback = serializers.CharField(
        required = False,
        allow_null = True
    )
    lead_category = serializers.CharField(
        max_length = 15,
        required = False,
        allow_null = True
    )
    profile_picture = Base64ImageField(
        required=False, allow_null=True
    )
    created_at = serializers.DateTimeField(
        read_only = True
    )
    updated_at = serializers.DateTimeField(
        read_only = True
    )
    permissions = PropertyPermissionRequestSerilizer()

    def create(self,validated_data) -> LeadCreateRequest:
        user_data = validated_data.pop('lead_assign_to')
        country_data = validated_data.pop('country')
        city_data = validated_data.pop('city')
        nationality_data = validated_data.pop('nationality')
        permission_data = validated_data.pop('permissions')

        lead_assign_to = user_data['user_id']
        country_id = country_data['country_id']
        city_id = city_data['city_id']
        nationality_id = nationality_data['nationality_id']

        permissions = Permissions(**permission_data)

        return LeadCreateRequest(
            lead_assign_to=lead_assign_to,
            country_id=country_id,
            city_id=city_id,
            nationality_id=nationality_id,
            permissions=permissions,
            **validated_data
        )
    


        

