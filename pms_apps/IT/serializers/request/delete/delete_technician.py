from rest_framework import serializers
from pms_apps.IT.dataclasses.request.delete.delete_technician import ITTechnicianDeleteRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class ITTechnicianDeleteRequestSerializer(serializers.Serializer):
    technician_id = serializers.IntegerField()

    def create(self, validated_data) -> ITTechnicianDeleteRequest:
        return ITTechnicianDeleteRequest(**validated_data)
    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='technician_id', description='ID of the IT technician',
                required=True, type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
        ]