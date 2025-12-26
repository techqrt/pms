from rest_framework import serializers
from pms_apps.activity_log.serializer.response.get_user import ActivityLogUserGetSerializer

class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()

class ActivityLogAdminGetSerializer(ActivityLogUserGetSerializer):
    user = UserGetSerializer(read_only = True)

class ActivityLogAdminResponseGetSerializer(serializers.Serializer):
    data = ActivityLogAdminGetSerializer()