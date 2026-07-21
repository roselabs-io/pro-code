from sqlalchemy import select

from app.models.author import Role
from app.models.invitation import Invitation


async def _token_for(db, email: str) -> str:
    result = await db.execute(select(Invitation).where(Invitation.email == email))
    return result.scalar_one().token


async def test_non_admin_cannot_invite(client, make_author, auth_header) -> None:
    author = await make_author()  # role: author
    resp = await client.post(
        "/invites", json={"email": "x@x.io"}, headers=auth_header(author)
    )
    assert resp.status_code == 403


async def test_invite_accept_then_login(client, db, make_author, auth_header) -> None:
    admin = await make_author(email="admin@x.io", role=Role.admin)
    await client.post("/invites", json={"email": "new@x.io"}, headers=auth_header(admin))

    token = await _token_for(db, "new@x.io")
    accepted = await client.post(
        "/invites/accept",
        json={"token": token, "display_name": "New", "password": "pw-abcdef"},
    )
    assert accepted.status_code == 200
    assert accepted.json()["access_token"]

    login = await client.post(
        "/auth/login", json={"email": "new@x.io", "password": "pw-abcdef"}
    )
    assert login.status_code == 200


async def test_accept_with_bad_token_is_400(client) -> None:
    resp = await client.post(
        "/invites/accept",
        json={"token": "nope", "display_name": "X", "password": "pw-abcdef"},
    )
    assert resp.status_code == 400


async def test_accept_twice_fails(client, db, make_author, auth_header) -> None:
    admin = await make_author(email="admin@x.io", role=Role.admin)
    await client.post("/invites", json={"email": "dup@x.io"}, headers=auth_header(admin))
    token = await _token_for(db, "dup@x.io")

    first = await client.post(
        "/invites/accept",
        json={"token": token, "display_name": "D", "password": "pw-abcdef"},
    )
    assert first.status_code == 200
    second = await client.post(
        "/invites/accept",
        json={"token": token, "display_name": "D2", "password": "pw-abcdef"},
    )
    assert second.status_code == 400


async def test_list_authors_is_admin_only(client, make_author, auth_header) -> None:
    author = await make_author(email="a@x.io")
    admin = await make_author(email="admin@x.io", role=Role.admin)

    assert (await client.get("/authors", headers=auth_header(author))).status_code == 403

    resp = await client.get("/authors", headers=auth_header(admin))
    assert resp.status_code == 200
    emails = [a["email"] for a in resp.json()]
    assert "admin@x.io" in emails
    assert "a@x.io" in emails
