import datetime as dt
from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_session
from app.services.public import PublicService

router = APIRouter(tags=["rss"])


def _rfc822(value: dt.datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone(dt.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")


@router.get("/rss")
async def rss(session: AsyncSession = Depends(get_session)) -> Response:
    posts = await PublicService(session).list_published(50, None)
    items = "".join(
        "<item>"
        f"<title>{escape(post.title)}</title>"
        f"<link>{escape(settings.site_url)}/posts/{escape(post.slug)}</link>"
        f"<guid>{escape(settings.site_url)}/posts/{escape(post.slug)}</guid>"
        f"<pubDate>{_rfc822(post.published_at)}</pubDate>"
        f"<description>{escape(post.excerpt)}</description>"
        "</item>"
        for post in posts
    )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0"><channel>'
        "<title>roselabs · field notes</title>"
        f"<link>{escape(settings.site_url)}</link>"
        "<description>Articles from roselabs.</description>"
        f"{items}"
        "</channel></rss>"
    )
    return Response(content=body, media_type="application/rss+xml")
