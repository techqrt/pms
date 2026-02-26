from rest_framework import serializers
from pms_apps.collection.serializers.response.get.get_employee import CollectionEmployeeGetSerializer


class CollectionEmployeeGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=CollectionEmployeeGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class CollectionEmployeeResponseGetAllSerializer(serializers.Serializer):
    data = CollectionEmployeeGetAllSerializer()