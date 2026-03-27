from rest_framework import serializers
from pms_apps.marketing.dataclasses.request.create.create_comment import MarketingCommentCreateRequest


class MarketingCommentCreateRequestSerializer(serializers.Serializer):
    targetType = serializers.ChoiceField(choices=['tenant', 'landlord'])
    targetId = serializers.IntegerField()
    content = serializers.CharField(max_length=5000)
    parentCommentId = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data) -> MarketingCommentCreateRequest:
        return MarketingCommentCreateRequest(
            target_type=validated_data['targetType'],
            target_id=validated_data['targetId'],
            content=validated_data['content'],
            created_by=None,  # Will be set from request user
            parent_comment_id=validated_data.get('parentCommentId')
        )
