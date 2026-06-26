import uuid
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import ForeignKey

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"



class BookTag(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )
    tags: List[Tag] = Relationship(
        link_model=BookTag,
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(lt=5)
    review_text: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"



class Follower(SQLModel, table=True):
    __tablename__ = "followers"
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    
    # user who follows
    follower_id: uuid.UUID = Field(foreign_key="users.uid")
    
    # user being followed
    following_id: uuid.UUID = Field(foreign_key="users.uid")
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    def __repr__(self):
        return f"<Follower {self.follower_id} -> {self.following_id}>"
    
    
    
    
    
class Post(SQLModel, table=True):
    __tablename__ = "posts"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    caption: Optional[str] = Field(default=None)
    user_uid: uuid.UUID = Field(foreign_key="users.uid")
    created_at: datetime = Field(default_factory=datetime.now)
    user: Optional["User"] = Relationship()
    images: List["PostImage"] = Relationship(back_populates="post", sa_relationship_kwargs={"cascade": "all, delete-orphan"}

)
    comments:  List["Comment"] = Relationship(back_populates="post", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    likes: List["PostLike"] = Relationship(back_populates="post", sa_relationship_kwargs={"cascade": "all, delete-orphan"})    
    def __repr__(self):
        return f"<Post {self.uid} by {self.user_uid}>"
    
    
    
class PostImage(SQLModel, table=True):
    __tablename__ = "post_images"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    image_url: str
    post_uid: uuid.UUID = Field(sa_column=Column(pg.UUID, ForeignKey("posts.uid", ondelete="CASCADE"), nullable=False))
    post: Optional[Post] = Relationship(back_populates="images")
    
    def __repr__(self):
        return f"<PostImage {self.image_url}>"
    
    
    
class PostLike(SQLModel, table=True):
    __tablename__ = "post_likes"
    user_uid: uuid.UUID = Field(foreign_key="users.uid", primary_key=True)
    post_uid: uuid.UUID = Field(foreign_key="posts.uid", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    post: Optional[Post] = Relationship(back_populates="likes")
    
    def __repr__(self):
        return f"<Like user={self.user_uid} post={self.post_uid}>"
    
    
class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    user_uid: uuid.UUID = Field(foreign_key="users.uid")
    post_uid: uuid.UUID = Field(foreign_key="posts.uid")
    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="comments.uid")
    created_at: datetime = Field(default_factory=datetime.now)
    post: Optional[Post] = Relationship(back_populates="comments")
    
    
    def __repr__(self):
        return f"<Comment {self.uid} post={self.post_uid}>"