from .get import LeadGetSerializer
from rest_framework import serializers


class LeadGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=LeadGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()

class LeadResponseGetAllSerilizer(serializers.Serializer):
    data = LeadGetAllSerializer()