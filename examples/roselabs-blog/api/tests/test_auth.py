from app.core.security import hash_password
from app.models.author import Author, Role

PASSWORD = "s3cret-pass"


async def _seed_author(db, email: str = "ada@roselabs.io") -> Author:
    author = Author(
        email=email,
        display_name="Ada",
        role=Role.author,
        password_hash=hash_password(PASSWORD),
    )
    db.add(author)
    await db.commit()
    return author


async def test_login_success_returns_token(client, db) -> None:
    await _seed_author(db)
    resp = await client.post(
        "/auth/login", json={"email": "ada@roselabs.io", "password": PASSWORD}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


async def test_login_wrong_password_is_401_generic(client, db) -> None:
    await _seed_author(db)
    resp = await client.post(
        "/auth/login", json={"email": "ada@roselabs.io", "password": "wrong"}
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid email or password"


async def test_login_unknown_email_same_generic_message(client) -> None:
    # No user-exists oracle: unknown email and wrong password must be indistinguishable.
    resp = await client.post(
        "/auth/login", json={"email": "nobody@roselabs.io", "password": "x"}
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid email or password"


async def test_me_requires_a_token(client) -> None:
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


async def test_me_rejects_a_bad_token(client) -> None:
    resp = await client.get("/auth/me", headers={"Authorization": "Bearer not.a.jwt"})
    assert resp.status_code == 401


async def test_me_returns_author_without_password_hash(client, db) -> None:
    author = await _seed_author(db)
    login = await client.post(
        "/auth/login", json={"email": "ada@roselabs.io", "password": PASSWORD}
    )
    token = login.json()["access_token"]

    resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == str(author.id)
    assert body["email"] == "ada@roselabs.io"
    assert body["role"] == "author"
    assert "password_hash" not in body
