from rest_framework import serializers


class APiResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    message = serializers.CharField()
