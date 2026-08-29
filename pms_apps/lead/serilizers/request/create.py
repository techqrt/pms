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
    lead_assign_to = UserRequestSerilizer(
        required = False,
        allow_null = True
    )
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
        max_length = 20,
        required = False,
        allow_null = True,
        allow_blank = True
    )
    address = serializers.CharField(
        required = False,
        allow_null = True,
        allow_blank = True
    )
    country = CountryRequestSerializer(
        required = False,
        allow_null = True
    )
    city = CityRequestSerializer(
        required = False,
        allow_null = True
    )
    nationality = NationalityRequestSerializer(
        required = False,
        allow_null = True
    )
    passport_or_id = serializers.CharField(
        max_length = 50,
        required = False,
        allow_null = True,
        allow_blank = True
    )
    civil_id = serializers.CharField(
        max_length = 50,
        required = False,
        allow_null = True,
        allow_blank = True
    )
    purpose = serializers.CharField(
        max_length = 10
    )
    po_box = serializers.CharField(
        max_length = 20,
        required = False,
        allow_null = True,
        allow_blank = True
    )
    feedback = serializers.CharField(
        required = False,
        allow_null = True,
        allow_blank = True
    )
    lead_category = serializers.CharField(
        max_length = 15
    )
    estimated_closing_date = serializers.DateField(
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
    permissions = PropertyPermissionRequestSerilizer(
        required = False,
        allow_null = True
    )

    def create(self,validated_data) -> LeadCreateRequest:
        user_data = validated_data.pop('lead_assign_to', None)
        country_data = validated_data.pop('country', None)
        city_data = validated_data.pop('city', None)
        nationality_data = validated_data.pop('nationality', None)
        permission_data = validated_data.pop('permissions', None)
        address = validated_data.pop('address', None)

        lead_assign_to = user_data['user_id'] if user_data else None
        country_id = country_data['country_id'] if country_data else None
        city_id = city_data['city_id'] if city_data else None
        nationality_id = nationality_data['nationality_id'] if nationality_data else None

        permissions = Permissions(**(permission_data or {}))

        return LeadCreateRequest(
            lead_assign_to=lead_assign_to,
            address=address,
            country_id=country_id,
            city_id=city_id,
            nationality_id=nationality_id,
            permissions=permissions,
            **validated_data
        )
    


        

