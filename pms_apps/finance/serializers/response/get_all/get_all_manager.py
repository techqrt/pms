from rest_framework import serializers
from pms_apps.finance.serializers.response.get.get_manager import FinanceManagerGetSerializer


class FinanceManagerGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=FinanceManagerGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class FinanceManagerResponseGetAllSerializer(serializers.Serializer):
    data = FinanceManagerGetAllSerializer()