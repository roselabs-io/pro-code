from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin
from app.core.db import get_session
from app.models.author import Author
from app.repositories.authors import AuthorRepository
from app.schemas.author import AuthorOut

router = APIRouter(tags=["authors"])


@router.get("/authors", response_model=list[AuthorOut])
async def list_authors(
    admin: Author = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
) -> list[Author]:
    return await AuthorRepository(session).list_all()
