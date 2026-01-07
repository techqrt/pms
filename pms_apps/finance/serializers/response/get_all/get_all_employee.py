from rest_framework import serializers
from pms_apps.finance.serializers.response.get.get_employee import FinanceEmployeeGetSerializer


class FinanceEmployeeGetAllSerializer(serializers.Serializer):
    data = serializers.ListField(child=FinanceEmployeeGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()


class FinanceEmployeeResponseGetAllSerializer(serializers.Serializer):
    data = FinanceEmployeeGetAllSerializer()