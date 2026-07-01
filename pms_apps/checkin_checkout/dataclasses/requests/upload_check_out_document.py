from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CheckOutDocumentUploadRequest:
    check_out_id: int
    document_type: str
    file: str
    linked_to_label: Optional[str] = None
    expiry_date: Optional[date] = None
    user_id: int = None
