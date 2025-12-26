from rest_framework import serializers


class ActivityLogUserGetSerializer(serializers.Serializer):
    logId = serializers.IntegerField(read_only = True)
    ipAddress = serializers.CharField(read_only = True)
    userAgent = serializers.CharField(read_only = True)
    action = serializers.CharField(read_only = True)
    model = serializers.CharField(read_only = True)
    method = serializers.CharField(read_only = True)
    endPoint = serializers.CharField(read_only = True)
    details = serializers.JSONField(read_only = True)
    createdOn = serializers.DateTimeField(read_only = True)

class ActivityLogUserResponseGetSerializer(serializers.Serializer):
    data = ActivityLogUserGetSerializer()