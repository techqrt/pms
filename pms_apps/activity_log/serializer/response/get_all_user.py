from rest_framework import serializers
from pms_apps.activity_log.serializer.response.get_user import ActivityLogUserGetSerializer

class ActivityLogUserGetAllSerilizer(serializers.Serializer):
    data = serializers.ListField(child=ActivityLogUserGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()

class ActivityLogUserResponseGetAllSerilizer(serializers.Serializer):
    data = ActivityLogUserGetAllSerilizer()