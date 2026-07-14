from rest_framework import serializers
from pms_apps.lead.serilizers.request.create import UserRequestSerilizer,CountryRequestSerializer,CityRequestSerializer,NationalityRequestSerializer
from pms_apps.lead.dataclasses.request.update import LeadUpdateRequest
from pms_apps.lead.serilizers.request.create import PropertyPermissionRequestSerilizer
from pms_apps.lead.dataclasses.request.update import PropertyPermissionUpdateRequest
from pms_apps.property.serializers.fields import Base64ImageField

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
    country = CountryRequestSerializer(required=False)
    city = CityRequestSerializer(required=False)
    nationality = NationalityRequestSerializer(required=False)
    passport_or_id = serializers.CharField(
        max_length = 50,required=False
    )
    purpose = serializers.CharField(
        max_length = 10,required=False
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
    is_active = serializers.BooleanField(
        required=False
    )
    email = serializers.EmailField(required=False, allow_null=True)
    profile_picture = Base64ImageField(
        required=False, allow_null=True
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
        country_data = validated_data.pop('country',{})
        city_data = validated_data.pop('city',{})
        nationality_data = validated_data.pop('nationality',{})
        permissions_data = validated_data.pop('permissions',{})

        lead_assign_to = user_data.get('user_id',None)
        country_id = country_data.get('country_id',None)
        city_id = city_data.get('city_id',None)
        nationality_id = nationality_data.get('nationality_id',None)
        property_permission = PropertyPermissionUpdateRequest(**permissions_data)
        return LeadUpdateRequest(
            lead_assign_to=lead_assign_to,
            country_id=country_id,
            city_id=city_id,
            nationality_id=nationality_id,
            property_permission = property_permission,
            **validated_data
        )