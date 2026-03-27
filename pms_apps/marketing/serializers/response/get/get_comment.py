from rest_framework import serializers


class UserCommentSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    name = serializers.CharField()
    phoneNumber = serializers.CharField()
    department = serializers.CharField()


class MarketingCommentReplySerializer(serializers.Serializer):
    commentId = serializers.IntegerField()
    content = serializers.CharField()
    createdBy = UserCommentSerializer()
    createdAt = serializers.DateTimeField()


class MarketingCommentResponseSerializer(serializers.Serializer):
    commentId = serializers.IntegerField()
    targetType = serializers.CharField()
    targetId = serializers.IntegerField()
    content = serializers.CharField()
    createdBy = UserCommentSerializer()
    createdAt = serializers.DateTimeField()
    replies = MarketingCommentReplySerializer(many=True)


class MarketingCommentCreateResponseSerializer(serializers.Serializer):
    data = MarketingCommentResponseSerializer()


class MarketingCommentGetAllDataSerializer(serializers.Serializer):
    data = serializers.ListField(child=MarketingCommentResponseSerializer())
    presentPage = serializers.IntegerField()
    totalPage = serializers.IntegerField()
    nextPageUrl = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    previousPageUrl = serializers.CharField(allow_null=True, required=False, allow_blank=True)


class MarketingCommentGetAllResponseSerializer(serializers.Serializer):
    data = MarketingCommentGetAllDataSerializer()
