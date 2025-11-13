from rest_framework import serializers
from pms_apps.lead.serilizers.request.create import UserRequestSerilizer,CountryRequestSerilizer
from pms_apps.lead.dataclasses.request.update import LeadUpdateRequest


class LeadUpdateRequestSerilizer(serializers.Serializer):
    lead_id = serializers.IntegerField()
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

    def create(self,validated_data) -> LeadUpdateRequest:
        user_data = validated_data.pop('lead_assign_to')
        country_data = validated_data.pop('nationality')
        lead_assign_to = user_data['user_id']
        nationality = country_data['country_id']
        return LeadUpdateRequest(
            lead_assign_to=lead_assign_to,
            nationality=nationality,
            **validated_data
        )