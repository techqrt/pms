from rest_framework import serializers


class GetSerializer(serializers.Serializer):
    values = serializers.CharField(max_length=100, required=False, default='')
