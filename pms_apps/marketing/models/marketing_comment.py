from django.db import models
from django.utils import timezone
from pms_apps.authentication.models import User


class MarketingComment(models.Model):
    TARGET_CHOICES = [
        ("tenant", "Tenant"),
        ("landlord", "Landlord"),
    ]

    comment_id = models.AutoField(primary_key=True)
    target_type = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES
    )
    target_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments_received"
    )
    content = models.TextField()
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments_created"
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "marketing_comment"
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment #{self.comment_id} on {self.target_type} - {self.target_id.name}"

    @staticmethod
    def create(
        target_type: str,
        target_id: int,
        content: str,
        created_by: int,
        parent_comment_id: int = None
    ) -> int:
        """Create a new comment and return its ID"""
        comment = MarketingComment()
        comment.target_type = target_type
        comment.target_id_id = target_id
        comment.content = content
        comment.created_by_id = created_by
        if parent_comment_id:
            comment.parent_comment_id = parent_comment_id
        comment.created_at = timezone.now()
        comment.save()
        return comment.comment_id

    @staticmethod
    def get_all_comments(target_type: str, target_id: int, parent_comment_id: int = None):
        """Get all comments for a specific target, optionally filtered by parent"""
        query = MarketingComment.objects.filter(
            target_type=target_type,
            target_id=target_id,
            parent_comment__isnull=True  # Only top-level comments
        ).select_related('created_by', 'target_id').prefetch_related('replies').order_by('-created_at')
        
        return query
