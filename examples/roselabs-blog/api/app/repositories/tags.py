from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.slug import slugify
from app.models.tag import Tag


class TagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create_many(self, names: list[str]) -> list[Tag]:
        resolved: dict[str, Tag] = {}
        for raw in names:
            name = raw.strip()
            if not name:
                continue
            slug = slugify(name)
            if slug in resolved:
                continue
            result = await self.session.execute(select(Tag).where(Tag.slug == slug))
            tag = result.scalar_one_or_none()
            if tag is None:
                tag = Tag(name=name, slug=slug)
                self.session.add(tag)
                await self.session.flush()
            resolved[slug] = tag
        return list(resolved.values())
