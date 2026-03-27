import dataclasses


@dataclasses.dataclass
class MarketingCommentCreateRequest:
    target_type: str
    target_id: int
    content: str
    created_by: int
    parent_comment_id: int = None
