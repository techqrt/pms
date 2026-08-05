from rest_framework import serializers
from pms_apps.lead.serilizers.request.create import UserRequestSerilizer,CountryRequestSerializer,CityRequestSerializer,NationalityRequestSerializer
from pms_apps.lead.dataclasses.request.update import LeadUpdateRequest
from pms_apps.lead.serilizers.request.create import PropertyPermissionRequestSerilizer
from pms_apps.lead.dataclasses.request.update import PropertyPermissionUpdateRequest
from pms_apps.property.serializers.fields import Base64ImageField
from pms_apps.common.sentinels import NOT_PROVIDED

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
    country = CountryRequestSerializer(required=False)
    city = CityRequestSerializer(required=False)
    nationality = NationalityRequestSerializer(required=False)
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
        max_length = 10,required=False
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
        max_length = 15,
        required = False,
        allow_null = True,
        allow_blank = True
    )
    estimated_closing_date = serializers.DateField(
        required = False,
        allow_null = True
    )
    is_active = serializers.BooleanField(
        required=False
    )
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phone_number = serializers.CharField(
        max_length = 20,
        required = False,
        allow_null = True,
        allow_blank = True
    )
    profile_picture = Base64ImageField(
        required=False, allow_null=True
    )
    tenant_code = serializers.CharField(
        max_length = 100,
        required = False,
        allow_null = True,
        allow_blank = True
    )
    created_at = serializers.DateTimeField(
        read_only = True,required=False
    )
    updated_at = serializers.DateTimeField(
        read_only = True,required=False
    )
    permissions = PropertyPermissionRequestSerilizer(required=False)

    def create(self,validated_data) -> LeadUpdateRequest:
        user_data = validated_data.pop('lead_assign_to', None)
        country_data = validated_data.pop('country', None)
        city_data = validated_data.pop('city', None)
        nationality_data = validated_data.pop('nationality', None)
        permissions_data = validated_data.pop('permissions',{})

        lead_assign_to = user_data.get('user_id') if user_data is not None else NOT_PROVIDED
        country_id = country_data.get('country_id') if country_data is not None else NOT_PROVIDED
        city_id = city_data.get('city_id') if city_data is not None else NOT_PROVIDED
        nationality_id = nationality_data.get('nationality_id') if nationality_data is not None else NOT_PROVIDED
        property_permission = PropertyPermissionUpdateRequest(**permissions_data)
        return LeadUpdateRequest(
            lead_assign_to=lead_assign_to,
            country_id=country_id,
            city_id=city_id,
            nationality_id=nationality_id,
            property_permission = property_permission,
            **validated_data
        )