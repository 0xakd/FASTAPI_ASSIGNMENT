import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PostImageModel(BaseModel):
    id: uuid.UUID
    image_url: str
    class Config:
        from_attributes = True   


class CommentModel(BaseModel):
    uid: uuid.UUID
    content: str
    user_uid: uuid.UUID
    parent_id: uuid.UUID | None
    created_at: datetime
    class Config:
        from_attributes = True


class Post(BaseModel):
    uid: uuid.UUID
    caption: Optional[str]
    user_uid: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True


class PostDetailModel(Post):
    images: List[PostImageModel] = []
    comments: List[CommentModel] = []
    likes_count: int = 0
    class Config:
        from_attributes = True


class PostCreateModel(BaseModel):
    caption: Optional[str]
    images: List[str] = []


class PostUpdateModel(BaseModel):
    caption: Optional[str]