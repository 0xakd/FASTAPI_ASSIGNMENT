from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.db.main import get_session
from src.errors import PostNotFound, MaxImagesExceeded, CommentNotFound

from .schemas import Post, PostCreateModel, PostUpdateModel
from .service import PostService

post_router = APIRouter()
post_service = PostService()

access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "author", "user"]))


@post_router.get("/", response_model=List[Post], dependencies=[role_checker])
async def get_posts(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    return await post_service.get_all_posts(session)


@post_router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_post(
    data: PostCreateModel,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(access_token_bearer),
):
    user_uid = token.get("user")["user_uid"]

    result = await post_service.create_post(data, user_uid, session)

    if result == "max_images":
        raise MaxImagesExceeded()

    return result


@post_router.get("/{post_uid}", response_model=Post, dependencies=[role_checker])
async def get_post(
    post_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    post = await post_service.get_post(post_uid, session)

    if not post:
        raise PostNotFound()

    return post


@post_router.patch("/{post_uid}", response_model=Post, dependencies=[role_checker])
async def update_post(
    post_uid: str,
    data: PostUpdateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    post = await post_service.update_post(post_uid, data, session)

    if not post:
        raise PostNotFound()

    return post


@post_router.delete(
    "/{post_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker]
)


async def delete_post(
    post_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    post = await post_service.get_post(post_uid, session)
    
    if not post:
        raise PostNotFound()
    await post_service.delete_post(post_uid, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)