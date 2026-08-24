from app.models.author import Role


async def _publish(client, headers, title="A Post") -> str:
    created = await client.post(
        "/posts", json={"title": title, "content_html": "<p>b</p>"}, headers=headers
    )
    await client.post(f"/posts/{created.json()['id']}/publish", headers=headers)
    return created.json()["slug"]


async def _submit(client, slug, body="Nice post", name="Ada"):
    return await client.post(
        f"/public/posts/{slug}/comments",
        json={"author_name": name, "author_email": "a@x.io", "body": body},
    )


async def _pending_id(client, headers) -> str:
    return (await client.get("/comments/pending", headers=headers)).json()[0]["id"]


async def test_submit_comment_is_pending_and_hidden(
    client, make_author, auth_header
) -> None:
    author = await make_author()
    slug = await _publish(client, auth_header(author))

    resp = await _submit(client, slug, body="hello")

    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"
    detail = await client.get(f"/public/posts/{slug}")
    assert detail.json()["comments"] == []


async def test_approved_comment_appears_publicly(
    client, make_author, auth_header
) -> None:
    author = await make_author()
    h = auth_header(author)
    slug = await _publish(client, h)
    await _submit(client, slug, body="approve me")

    approved = await client.post(
        f"/comments/{await _pending_id(client, h)}/approve", headers=h
    )

    assert approved.status_code == 200
    detail = await client.get(f"/public/posts/{slug}")
    assert "approve me" in [c["body"] for c in detail.json()["comments"]]


async def test_hidden_comment_never_public(client, make_author, auth_header) -> None:
    author = await make_author()
    h = auth_header(author)
    slug = await _publish(client, h)
    await _submit(client, slug, body="hide me")

    await client.post(f"/comments/{await _pending_id(client, h)}/hide", headers=h)

    detail = await client.get(f"/public/posts/{slug}")
    assert detail.json()["comments"] == []


async def test_non_owner_cannot_moderate(client, make_author, auth_header) -> None:
    a = await make_author(email="a@x.io")
    b = await make_author(email="b@x.io")
    slug = await _publish(client, auth_header(a))
    await _submit(client, slug)
    cid = await _pending_id(client, auth_header(a))

    resp = await client.post(f"/comments/{cid}/approve", headers=auth_header(b))

    assert resp.status_code == 404
    assert (await client.get("/comments/pending", headers=auth_header(b))).json() == []


async def test_admin_can_moderate_any(client, make_author, auth_header) -> None:
    a = await make_author(email="a@x.io")
    admin = await make_author(email="admin@x.io", role=Role.admin)
    slug = await _publish(client, auth_header(a))
    await _submit(client, slug)
    cid = await _pending_id(client, auth_header(admin))

    resp = await client.post(f"/comments/{cid}/approve", headers=auth_header(admin))

    assert resp.status_code == 200


async def test_comment_body_stored_as_text(client, make_author, auth_header) -> None:
    author = await make_author()
    h = auth_header(author)
    slug = await _publish(client, h)
    payload = "<script>alert(1)</script>hi"
    await _submit(client, slug, body=payload)

    await client.post(f"/comments/{await _pending_id(client, h)}/approve", headers=h)

    detail = await client.get(f"/public/posts/{slug}")
    # Stored + returned verbatim as text; the client renders it escaped (React default).
    assert detail.json()["comments"][0]["body"] == payload


async def test_cannot_comment_on_a_draft(client, make_author, auth_header) -> None:
    author = await make_author()
    created = await client.post(
        "/posts",
        json={"title": "Draft", "content_html": "<p>x</p>"},
        headers=auth_header(author),
    )

    resp = await _submit(client, created.json()["slug"])

    assert resp.status_code == 404
