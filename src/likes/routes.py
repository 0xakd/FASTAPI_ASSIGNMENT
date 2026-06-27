from fastapi import APIRouter, Depends, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker

from src.posts.service import PostService
from src.errors import PostNotFound

from .service import LikeService

like_router = APIRouter()
like_service = LikeService()
post_service = PostService()

access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "author", "user"]))


@like_router.post(
    "/{post_uid}/like",
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def like_post(
    post_uid: str,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(access_token_bearer),
):
    user_uid = token.get("user")["user_uid"]

    post = await post_service.get_post(post_uid, session)
    if not post:
        raise PostNotFound()

    await like_service.like_post(post_uid, user_uid, session)
    return {"message": "Post liked"}


@like_router.delete(
    "/{post_uid}/like",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker],
)
async def unlike_post(
    post_uid: str,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(access_token_bearer),
):
    user_uid = token.get("user")["user_uid"]

    post = await post_service.get_post(post_uid, session)
    if not post:
        raise PostNotFound()

    result = await like_service.unlike_post(post_uid, user_uid, session)

    if not result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(status_code=status.HTTP_204_NO_CONTENT)