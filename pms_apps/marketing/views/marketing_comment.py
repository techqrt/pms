from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status

from pms_apps.common.common import Common
from pms_apps.common.utils import Utils
from pms_apps.authentication.models import User
from pms_apps.marketing.models.marketing_comment import MarketingComment
from pms_apps.marketing.dataclasses.request.create.create_comment import MarketingCommentCreateRequest
from pms_apps.marketing.serializers.response.get.get_comment import (
    MarketingCommentCreateResponseSerializer,
    MarketingCommentGetAllResponseSerializer
)


class MarketingCommentView:
    def __init__(self):
        self.comment_create = "Comment added successfully"
        self.data_get = "Comments fetched successfully"
        self.data_no_match = "No matching records found"
        self.error = "Something went wrong"

    @Common(response_handler=MarketingCommentCreateResponseSerializer).exception_handler
    def create_comment_extract(self, params: MarketingCommentCreateRequest, user_id: int):
        """Create a new comment"""
        with transaction.atomic():
            # Validate target user exists
            target_user = User.objects.filter(user_id=params.target_id).first()
            if not target_user:
                raise ValueError("Target user not found")
            
            # Validate created_by user exists
            created_by_user = User.objects.filter(user_id=user_id).first()
            if not created_by_user:
                raise ValueError("User not found")
            
            # If replying to a comment, validate parent comment exists
            if params.parent_comment_id:
                parent_comment = MarketingComment.objects.filter(
                    comment_id=params.parent_comment_id
                ).first()
                if not parent_comment:
                    raise ValueError("Parent comment not found")
            
            # Create comment
            comment_id = MarketingComment.create(
                target_type=params.target_type,
                target_id=params.target_id,
                content=params.content,
                created_by=user_id,
                parent_comment_id=params.parent_comment_id
            )
            
            # Fetch the created comment with related data
            comment = MarketingComment.objects.filter(
                comment_id=comment_id
            ).select_related('created_by', 'target_id', 'parent_comment').first()
            
            data = self._format_comment(comment)
        
        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.comment_create,
                data=data
            )
        )

    @Common(response_handler=MarketingCommentGetAllResponseSerializer).exception_handler
    def get_all_comments_extract(self, target_type: str, target_id: int, page: int = 1, page_size: int = 10):
        """Get all comments for a specific target"""
        with transaction.atomic():
            # Validate target user exists
            target_user = User.objects.filter(user_id=target_id).first()
            if not target_user:
                raise ValueError("Target user not found")
            
            # Validate target_type
            if target_type not in ['tenant', 'landlord']:
                raise ValueError("Invalid target type. Must be 'tenant' or 'landlord'")
            
            # Get comments
            comments_queryset = MarketingComment.get_all_comments(
                target_type=target_type,
                target_id=target_id
            )
            
            # Paginate
            paginator = Paginator(comments_queryset, per_page=page_size)
            
            if page > paginator.num_pages:
                raise ValueError('Page limit exceeded!')
            
            page_data = paginator.page(page)
            comments = list(page_data)
            
            # Format comments with replies
            data = [self._format_comment(comment) for comment in comments]
            
            # Add pagination parameters
            data = Utils.add_page_parameter(
                final_data=data,
                page_num=page,
                total_page=paginator.num_pages,
                present_url=None,
                next_page_required=True if paginator.num_pages != page else False
            )
        
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(
                message=self.data_get,
                data=data
            )
        )

    def _format_comment(self, comment):
        """Format a comment object with user details and nested replies"""
        replies = comment.replies.all() if comment.parent_comment_id is None else []
        
        return {
            "commentId": comment.comment_id,
            "targetType": comment.target_type,
            "targetId": comment.target_id.user_id,
            "content": comment.content,
            "createdBy": {
                "userId": comment.created_by.user_id,
                "name": comment.created_by.name,
                "phoneNumber": comment.created_by.phone_number,
                "department": comment.created_by.department
            },
            "createdAt": comment.created_at,
            "replies": [
                {
                    "commentId": reply.comment_id,
                    "content": reply.content,
                    "createdBy": {
                        "userId": reply.created_by.user_id,
                        "name": reply.created_by.name,
                        "phoneNumber": reply.created_by.phone_number,
                        "department": reply.created_by.department
                    },
                    "createdAt": reply.created_at
                }
                for reply in replies
            ]
        }
