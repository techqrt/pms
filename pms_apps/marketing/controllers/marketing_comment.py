from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pms_apps.common.swagger import SwaggerPage
from pms_apps.common.serializer_validations import SerializerValidations
from pms_apps.marketing.serializers.request.create.create_comment import MarketingCommentCreateRequestSerializer
from pms_apps.marketing.serializers.request.get.get_comment import MarketingCommentGetAllRequestSerializer
from pms_apps.marketing.serializers.response.get.get_comment import (
    MarketingCommentCreateResponseSerializer,
    MarketingCommentGetAllResponseSerializer
)
from pms_apps.marketing.views.marketing_comment import MarketingCommentView


class MarketingCommentViewController:
    @extend_schema(
        description="Create a comment on a tenant or landlord profile. Can also reply to existing comments.",
        request=MarketingCommentCreateRequestSerializer,
        responses=SwaggerPage.response(
            description=MarketingCommentView().comment_create)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingCommentCreateRequestSerializer).validate
    def create_comment(request: Request) -> Response:
        params = request.params
        params.created_by = request.user.user_id
        return MarketingCommentView().create_comment_extract(
            params=params,
            user_id=request.user.user_id
        )

    @extend_schema(
        description="Get all comments for a specific tenant or landlord with pagination. Returns both top-level comments and their replies.",
        parameters=MarketingCommentGetAllRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(
            response=MarketingCommentGetAllResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    @SerializerValidations(serializer=MarketingCommentGetAllRequestSerializer).validate
    def get_all_comments(request: Request) -> Response:
        # Extract custom fields from raw request before serializer processing
        target_type = request.GET.get('target_type')
        target_id = request.GET.get('target_id')
        
        params = request.params
        return MarketingCommentView().get_all_comments_extract(
            target_type=target_type,
            target_id=int(target_id) if target_id else None,
            page=params.page_num,
            page_size=params.limit
        )
