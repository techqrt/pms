from rest_framework import serializers


class SearchResponseSerializer(serializers.Serializer):
    data=serializers.ListField()
