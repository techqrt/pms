from rest_framework import serializers
from pms_apps.IT.serializers.request.create.create_manager import UserRequestSerializer
from pms_apps.IT.dataclasses.request.create.create_technician import ITTechnicianCreateRequest

class ITTechnicianCreateRequestSerializer(serializers.Serializer):
    technician_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    skill_area = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    tickets_closed = serializers.IntegerField(required=False, default=0)
    years_of_experience = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> ITTechnicianCreateRequest:
        technician_id_data = validated_data.pop('technician_id')
        validated_data['technician_id'] = technician_id_data['user_id']

        return ITTechnicianCreateRequest(**validated_data)