import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PostImageModel(BaseModel):
    id: uuid.UUID
    image_url: str


class CommentModel(BaseModel):
    uid: uuid.UUID
    content: str
    user_uid: uuid.UUID
    parent_id: Optional[uuid.UUID]
    created_at: datetime


class Post(BaseModel):
    uid: uuid.UUID
    caption: Optional[str]
    user_uid: uuid.UUID
    created_at: datetime


class PostDetailModel(Post):
    images: List[PostImageModel]
    comments: List[CommentModel]


class PostCreateModel(BaseModel):
    caption: Optional[str]
    images: List[str] = []


class PostUpdateModel(BaseModel):
    caption: Optional[str]