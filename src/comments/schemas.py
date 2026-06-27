import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class ReplyCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    uid: uuid.UUID
    content: str
    user_uid: uuid.UUID
    post_uid: uuid.UUID
    parent_id: Optional[uuid.UUID]
    created_at: datetime
    # replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


CommentResponse.model_rebuild()