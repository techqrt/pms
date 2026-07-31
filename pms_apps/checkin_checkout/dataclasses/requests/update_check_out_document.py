from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CheckOutDocumentUpdateRequest:
    check_out_document_id: int
    document_name: Optional[str] = None
    linked_to_label: Optional[str] = None
    expiry_date: Optional[date] = None
    user_id: Optional[int] = None


@dataclass
class CheckOutDocumentDeleteRequest:
    check_out_document_id: int
