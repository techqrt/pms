from rest_framework import serializers


class GetAllGeneralSerializer(serializers.Serializer):
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()
    totalCount = serializers.IntegerField()
