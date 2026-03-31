from rest_framework import serializers
from pms_apps.property.serializers.response.assignment_get import PropertyAssignmentResponseGetSerializer


class AssignmentGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=PropertyAssignmentResponseGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class PropertyAssignmentResponseGetAllSerializer(serializers.Serializer):
    data = AssignmentGetAllSerializer()
