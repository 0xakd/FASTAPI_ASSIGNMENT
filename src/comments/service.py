import uuid
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Comment, Post
from src.errors import BooklyException
from .schemas import CommentResponse


class CommentService:

    async def create_comment(
        self,
        post_id: uuid.UUID,
        user_id: uuid.UUID,
        content: str,
        session: AsyncSession
    ):
        post = await session.get(Post, post_id)
        if not post:
            raise BooklyException("Post not found")

        comment = Comment(
            content=content,
            user_uid=user_id,
            post_uid=post_id
        )

        session.add(comment)
        await session.commit()
        await session.refresh(comment)

        return CommentResponse(
            uid=comment.uid,
            content=comment.content,
            user_uid=comment.user_uid,
            post_uid=comment.post_uid,
            parent_id=comment.parent_id,
            created_at=comment.created_at,
            replies=[]
        )

    async def reply_to_comment(
        self,
        comment_id: uuid.UUID,
        user_id: uuid.UUID,
        content: str,
        session: AsyncSession
    ):
        parent = await session.get(Comment, comment_id)
        if not parent:
            raise BooklyException("Parent comment not found")

        reply = Comment(
            content=content,
            user_uid=user_id,
            post_uid=parent.post_uid,
            parent_id=comment_id
        )

        session.add(reply)
        await session.commit()
        await session.refresh(reply)

        return CommentResponse(
            uid=reply.uid,
            content=reply.content,
            user_uid=reply.user_uid,
            post_uid=reply.post_uid,
            parent_id=reply.parent_id,
            created_at=reply.created_at,
            replies=[]
        )

    async def get_post_comments(
        self,
        post_id: uuid.UUID,
        session: AsyncSession
    ):
        statement = select(Comment).where(
            Comment.post_uid == post_id,
        )

        result = await session.execute(statement)
        comments = result.scalars().all()
        return [CommentResponse(
            uid=c.uid,
            content=c.content,
            user_uid=c.user_uid,
            post_uid=c.post_uid,
            parent_id=c.parent_id,
            created_at=c.created_at,
            replies=[]
        )
            for c in comments
        ]

    async def delete_comment(
        self,
        comment_id: uuid.UUID,
        user_id: uuid.UUID,
        session: AsyncSession
    ):
        comment = await session.get(Comment, comment_id)

        if not comment:
            raise BooklyException("Comment not found")

        if comment.user_uid != user_id:
            raise BooklyException("Not authorized")

        await session.delete(comment)
        await session.commit()