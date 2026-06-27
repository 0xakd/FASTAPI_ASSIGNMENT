import uuid
from datetime import datetime
from pydantic import BaseModel


class LikeResponse(BaseModel):
    user_uid: uuid.UUID
    post_uid: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str