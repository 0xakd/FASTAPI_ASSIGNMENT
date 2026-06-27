from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import PostLike


class LikeService:

    async def like_post(self, post_uid: str, user_uid: str, session: AsyncSession):
        # prevent duplicate like
        statement = select(PostLike).where(
            PostLike.post_uid == post_uid,
            PostLike.user_uid == user_uid,
        )

        result = await session.execute(statement)
        existing = result.scalar_one_or_none()

        if existing:
            return existing  # already liked

        like = PostLike(user_uid=user_uid, post_uid=post_uid)
        session.add(like)
        await session.commit()
        return like

    async def unlike_post(self, post_uid: str, user_uid: str, session: AsyncSession):
        statement = select(PostLike).where(
            PostLike.post_uid == post_uid,
            PostLike.user_uid == user_uid,
        )

        result = await session.execute(statement)
        like = result.scalar_one_or_none()

        if not like:
            return None

        await session.delete(like)
        await session.commit()
        return True