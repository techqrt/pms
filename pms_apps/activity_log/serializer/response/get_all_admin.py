from rest_framework import serializers
from pms_apps.activity_log.serializer.response.get_admin import ActivityLogAdminGetSerializer

class ActivityLogAdminGetAllSerilizer(serializers.Serializer):
    data = serializers.ListField(child=ActivityLogAdminGetSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()

class ActivityLogAdminResponseGetAllSerilizer(serializers.Serializer):
    data = ActivityLogAdminGetAllSerilizer()