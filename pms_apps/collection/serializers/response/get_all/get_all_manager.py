from rest_framework import serializers
from pms_apps.collection.serializers.response.get.get_manager import CollectionManagerGetSerializer


class CollectionManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=CollectionManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class CollectionManagerResponseGetAllSerializer(serializers.Serializer):
    data = CollectionManagerGetAllSerializer()