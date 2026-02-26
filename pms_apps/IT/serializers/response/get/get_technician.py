from rest_framework import serializers
from pms_apps.IT.serializers.response.get.get_manager import UserGetSerializer

class ITTechnicianGetSerializer(serializers.Serializer):
    technicianId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    skillArea = serializers.CharField(read_only=True)
    ticketsClosed = serializers.IntegerField(read_only=True)
    yearsOfExperience = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)

class ITTechnicianResponseGetSerializer(serializers.Serializer):
    data = ITTechnicianGetSerializer()