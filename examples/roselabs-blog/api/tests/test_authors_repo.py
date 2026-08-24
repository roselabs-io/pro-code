from app.models.author import Author, Role
from app.repositories.authors import AuthorRepository


async def test_author_round_trip(session) -> None:
    repo = AuthorRepository(session)
    await repo.add(
        Author(
            email="ada@roselabs.io",
            display_name="Ada",
            role=Role.author,
            password_hash="hashed",
        )
    )

    fetched = await repo.get_by_email("ada@roselabs.io")

    assert fetched is not None
    assert fetched.display_name == "Ada"
    assert fetched.role is Role.author
    assert fetched.password_hash == "hashed"
