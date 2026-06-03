from datetime import datetime
from typing import List

from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Post, PostImage, Comment, PostLike
from .schemas import PostCreateModel, PostUpdateModel


class PostService:

    async def get_all_posts(self, session: AsyncSession):
        statement = select(Post).order_by(desc(Post.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_post(self, post_uid: str, session: AsyncSession):
        statement = select(Post).where(Post.uid == post_uid)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def create_post(self, data: PostCreateModel, user_uid: str, session: AsyncSession):
        post = Post(
            caption=data.caption,
            user_uid=user_uid,
        )

        session.add(post)
        await session.flush()  # needed to get post.uid

        # handle images
        if len(data.images) > 5:
            return "max_images"

        for img in data.images:
            session.add(PostImage(image_url=img, post_uid=post.uid))

        await session.commit()
        return post

    async def update_post(self, post_uid: str, data: PostUpdateModel, session: AsyncSession):
        post = await self.get_post(post_uid, session)

        if not post:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for k, v in update_data.items():
            setattr(post, k, v)

        await session.commit()
        return post

    async def delete_post(self, post_uid: str, session: AsyncSession):
        post = await self.get_post(post_uid, session)

        if not post:
            return None

        await session.delete(post)
        await session.commit()
        # return True

    async def like_post(self, post_uid: str, user_uid: str, session: AsyncSession):
        like = PostLike(user_uid=user_uid, post_uid=post_uid)
        session.add(like)
        await session.commit()
        return like

    async def unlike_post(self, post_uid: str, user_uid: str, session: AsyncSession):
        statement = select(PostLike).where(
            PostLike.post_uid == post_uid,
            PostLike.user_uid == user_uid,
        )

        result = await session.exec(statement)
        like = result.first()

        if not like:
            return None

        await session.delete(like)
        await session.commit()
        return {}

    async def add_comment(self, post_uid: str, user_uid: str, content: str, parent_id, session: AsyncSession):
        # validate parent (optional)
        if parent_id:
            parent = await session.get(Comment, parent_id)
            if not parent:
                return "parent_not_found"

        comment = Comment(
            content=content,
            user_uid=user_uid,
            post_uid=post_uid,
            parent_id=parent_id,
        )

        session.add(comment)
        await session.commit()
        return comment