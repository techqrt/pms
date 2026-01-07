from rest_framework import serializers
from pms_apps.helper_apis.serilizers.nationality.response.get import NationalityResponseGetSerializers
class NationalityGetAllSerilizers(serializers.Serializer):
    data = serializers.ListField(child=NationalityResponseGetSerializers())
    presentPage = serializers.IntegerField(read_only=True)
    totalPage = serializers.IntegerField(read_only=True)

class NationalityResponseGetAllSerilizers(serializers.Serializer):
    data = NationalityGetAllSerilizers(read_only = True)