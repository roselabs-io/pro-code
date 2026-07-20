import asyncio
import datetime as dt

from sqlalchemy import select

from app.core.db import SessionLocal
from app.core.log import log_event
from app.core.security import hash_password
from app.models.author import Author, Role
from app.models.post import Post, PostStatus

_SAMPLE_ARTICLE = """<!doctype html><html><head><meta charset="utf8"><style>
body{font-family:Georgia,serif;background:#faf9f5;color:#1a1a1a;padding:2rem;line-height:1.7;max-width:42rem;margin:auto}
h1{color:#7a4b2b} .box{border-left:4px solid #d99a5c;padding:.6rem 1rem;background:#fff;margin:1rem 0}
</style></head><body><h1>The Iframe Test</h1>
<p>This article ships its <em>own</em> CSS — a serif face, a cream background, a coloured rule.</p>
<div class="box">If the sandbox works, none of this styling leaks into the app shell around it,
and no script here can run.</div>
<p>That isolation is the whole point of decision 0001.</p>
</body></html>"""


async def _seed() -> None:
    async with SessionLocal() as session:
        existing = await session.execute(
            select(Author).where(Author.email == "demo@roselabs.io")
        )
        if existing.scalar_one_or_none() is not None:
            log_event("SEED_SKIPPED", reason="already_seeded")
            return

        author = Author(
            email="demo@roselabs.io",
            display_name="roselabs",
            role=Role.admin,
            password_hash=hash_password("demo-password-please-change"),
        )
        session.add(author)
        await session.flush()

        now = dt.datetime.now(dt.timezone.utc)
        session.add_all(
            [
                Post(
                    author_id=author.id,
                    title="Welcome to the roselabs blog",
                    slug="welcome",
                    content_html="<!doctype html><h1>Welcome</h1><p>The first published post.</p>",
                    excerpt="The first published post.",
                    status=PostStatus.published,
                    published_at=now,
                ),
                Post(
                    author_id=author.id,
                    title="The iframe test",
                    slug="the-iframe-test",
                    content_html=_SAMPLE_ARTICLE,
                    excerpt="A rich, self-contained article rendered in an isolated iframe.",
                    status=PostStatus.published,
                    published_at=now - dt.timedelta(minutes=1),
                ),
                Post(
                    author_id=author.id,
                    title="A secret draft",
                    slug="a-secret-draft",
                    content_html="<h1>Draft</h1><p>This must never appear publicly.</p>",
                    excerpt="unpublished",
                    status=PostStatus.draft,
                ),
            ]
        )
        await session.commit()
        log_event("SEED_DONE", authors=1, posts=3)


def main() -> None:
    asyncio.run(_seed())


if __name__ == "__main__":
    main()
