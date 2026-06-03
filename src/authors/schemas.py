# authors/schemas.py

import uuid
from datetime import datetime
from typing import List
# from src.auth.schemas import UserBooksModel
from pydantic import BaseModel


class AuthorModel(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    books_written: int = 0
    followers_count: int = 0
    following_count: int = 0


class AuthorListResponseModel(BaseModel):
    authors: List[AuthorModel]


class FollowResponseModel(BaseModel):
    message: str