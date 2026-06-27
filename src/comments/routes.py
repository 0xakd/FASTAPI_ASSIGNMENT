import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.comments.schemas import CommentCreate, ReplyCreate, CommentResponse
from src.comments.service import CommentService
from src.db.main import get_session
from src.auth.dependencies import get_current_user


comments_router = APIRouter()

comment_service = CommentService()


@comments_router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    post_id: uuid.UUID,
    data: CommentCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    return await comment_service.create_comment(
        post_id,
        user.uid,
        data.content,
        session
    )


@comments_router.post("/comments/{comment_id}/reply", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def reply_comment(
    comment_id: uuid.UUID,
    data: ReplyCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    return await comment_service.reply_to_comment(
        comment_id,
        user.uid,
        data.content,
        session
    )


@comments_router.get("/{post_id}/comments", response_model=list[CommentResponse])
async def get_comments(
    post_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await comment_service.get_post_comments(post_id, session)


@comments_router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    await comment_service.delete_comment(
        comment_id,
        user.uid,
        session
    )