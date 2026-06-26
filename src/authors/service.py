import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .schemas import AuthorModel

from src.db.models import User, Follower
from src.errors import (
    UserNotFound,
    AlreadyFollowing,
    NotFollowing,
    CannotFollowYourself,
)


class AuthorService:

    # helper: ensure user exists
    async def _get_user_or_fail(self, author_id: uuid.UUID, session: AsyncSession):
        result = await session.execute(
            select(User).where(User.uid == author_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFound()

        return user



    async def get_authors(self, session: AsyncSession):
        result = await session.execute(
            select(User).where(User.role == "author")
        )
        users = result.scalars().all()
        authors = []
        for user in users:
            followers_count = await session.scalar(
                select(func.count()).select_from(Follower)
                .where(Follower.following_id == user.uid)
            ) or 0
            following_count = await session.scalar(
                select(func.count()).select_from(Follower)
                .where(Follower.follower_id == user.uid)
            ) or 0
            authors.append(
                AuthorModel(
                    uid=user.uid,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    created_at=user.created_at,
                    followers_count=followers_count,
                    following_count=following_count
                )
            )
        return authors



    # Get single author
    async def get_author(self, author_id: uuid.UUID, session: AsyncSession):

        user = await self._get_user_or_fail(author_id, session)

        followers_count = await session.scalar(
            select(func.count()).where(Follower.following_id == user.uid)
        )

        following_count = await session.scalar(
            select(func.count()).where(Follower.follower_id == user.uid)
        )

        return {
            "uid": user.uid,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "created_at": user.created_at,
            "followers_count": followers_count or 0,
            "following_count": following_count or 0
        }


    # 🔹 Follow author
    async def follow_author(self, author_id, current_user, session):

        # ensure author exists
        await self._get_user_or_fail(author_id, session)

        # self-follow check
        if current_user.uid == author_id:
            raise CannotFollowYourself()

        # check existing follow
        existing = await session.execute(
            select(Follower).where(
                Follower.follower_id == current_user.uid,
                Follower.following_id == author_id
            )
        )

        if existing.scalar():
            raise AlreadyFollowing()

        # create follow
        follow = Follower(
            follower_id=current_user.uid,
            following_id=author_id
        )

        session.add(follow)
        await session.commit()
        return {"message": "Followed successfully"}


    # Unfollow author
    async def unfollow_author(self, author_id, current_user, session):
        # ensure author exists
        await self._get_user_or_fail(author_id, session)

        result = await session.execute(
            select(Follower).where(
                Follower.follower_id == current_user.uid,
                Follower.following_id == author_id
            )
        )

        follow = result.scalar_one_or_none()

        if not follow:
            raise NotFollowing()
        
        await session.delete(follow)
        await session.commit()
        return {"message": "Unfollowed successfully"}