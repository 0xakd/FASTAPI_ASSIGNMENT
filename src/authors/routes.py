import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
from src.auth.dependencies import get_current_user
from src.db.models import User

from .service import AuthorService
from .schemas import AuthorModel, AuthorListResponseModel, FollowResponseModel

authors_router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

author_service = AuthorService()

# GET ALL AUTHORS 
@authors_router.get(
    "/",
    response_model=AuthorListResponseModel,
    status_code=status.HTTP_200_OK
)
async def get_authors(
    session: AsyncSession = Depends(get_session)
):
    """
    Fetch all authors with follower/following counts
    """
    authors = await author_service.get_authors(session)
    return {"authors": authors}

#GET SINGLE AUTHOR
@authors_router.get(
    "/{author_id}",
    response_model=AuthorModel,
    status_code=status.HTTP_200_OK
)
async def get_author(
    author_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    """
    Fetch details of a single author
    """
    return await author_service.get_author(author_id, session)


# 🔹 Follow author (AUTH REQUIRED)
@authors_router.post(
    "/{author_id}/follow",
    response_model=FollowResponseModel,
    status_code=status.HTTP_201_CREATED
)
async def follow_author(
    author_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Follow an author

    Requires JWT authentication
    """
    return await author_service.follow_author(
        author_id,
        current_user,
        session
    )


# 🔹 Unfollow author (AUTH REQUIRED)
@authors_router.delete(
    "/{author_id}/follow",
    status_code=status.HTTP_204_NO_CONTENT
)
async def unfollow_author(
    author_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Unfollow an author

    Returns no content on success
    """
    await author_service.unfollow_author(
        author_id,
        current_user,
        session
    )
    return None 