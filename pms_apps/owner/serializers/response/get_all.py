from rest_framework import serializers
from pms_apps.owner.serializers.response.get import OwnerGetSerializer


class OwnerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=OwnerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class OwnerResponseGetAllSerializer(serializers.Serializer):
    data = OwnerGetAllSerializer()