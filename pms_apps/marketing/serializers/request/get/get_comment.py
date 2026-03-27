from rest_framework import serializers
from pms_apps.common.serializers.request.get_all import GetAllSerializer
from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.dataclasses.request.get_all import GetAll
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from datetime import datetime, time
from django.utils import timezone


class MarketingCommentGetAllRequestSerializer(GetAllSerializer):
    target_type = serializers.ChoiceField(choices=['tenant', 'landlord'], required=True)
    target_id = serializers.IntegerField(required=True)

    def create(self, validated_data) -> GetAll:
        # Extract custom fields before passing to GetAll
        validated_data.pop('target_type', None)
        validated_data.pop('target_id', None)
        
        # Handle date field conversions (from parent class pattern)
        from_date = validated_data.get('from_date', None)
        to_date = validated_data.get('to_date', None)
        if from_date:
            validated_data['from_date'] = timezone.make_aware(
                value=datetime.combine(date=from_date, time=time.min))
        if to_date:
            validated_data['to_date'] = timezone.make_aware(
                value=datetime.combine(date=to_date, time=time.max))
        
        return GetAll(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_all_parameters()) -> list:
        default_parameters.append(OpenApiParameter(
            name='target_type', description='Target type - tenant or landlord',
            required=True, type=OpenApiTypes.STR,
            enum=['tenant', 'landlord'],
            location=OpenApiParameter.QUERY
        ))
        default_parameters.append(OpenApiParameter(
            name='target_id', description='User ID of the target',
            required=True, type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY
        ))
        return default_parameters
