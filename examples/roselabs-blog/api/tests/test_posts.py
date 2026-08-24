from app.models.author import Role


async def _create_post(client, headers, title="Hello World", content="<p>hi</p>") -> dict:
    resp = await client.post(
        "/posts", json={"title": title, "content_html": content}, headers=headers
    )
    assert resp.status_code == 201
    return resp.json()


async def test_create_draft(client, make_author, auth_header) -> None:
    author = await make_author()
    body = await _create_post(client, auth_header(author))
    assert body["status"] == "draft"
    assert body["slug"] == "hello-world"
    assert body["author_id"] == str(author.id)
    assert body["published_at"] is None


async def test_create_requires_auth(client) -> None:
    resp = await client.post("/posts", json={"title": "x", "content_html": "<p>x</p>"})
    assert resp.status_code == 401


async def test_list_mine_returns_only_own_posts(client, make_author, auth_header) -> None:
    a = await make_author(email="a@x.io")
    b = await make_author(email="b@x.io")
    await _create_post(client, auth_header(a), title="A post")
    await _create_post(client, auth_header(b), title="B post")

    resp = await client.get("/posts/mine", headers=auth_header(a))

    assert resp.status_code == 200
    assert [p["title"] for p in resp.json()] == ["A post"]


async def test_non_owner_cannot_get_update_or_delete(
    client, make_author, auth_header
) -> None:
    a = await make_author(email="a@x.io")
    b = await make_author(email="b@x.io")
    post = await _create_post(client, auth_header(a))
    pid = post["id"]
    hb = auth_header(b)

    assert (await client.get(f"/posts/{pid}", headers=hb)).status_code == 404
    assert (
        await client.patch(f"/posts/{pid}", json={"title": "hax"}, headers=hb)
    ).status_code == 404
    assert (await client.delete(f"/posts/{pid}", headers=hb)).status_code == 404


async def test_owner_can_update_and_delete(client, make_author, auth_header) -> None:
    a = await make_author()
    post = await _create_post(client, auth_header(a))
    pid = post["id"]
    h = auth_header(a)

    updated = await client.patch(f"/posts/{pid}", json={"title": "Renamed"}, headers=h)
    assert updated.status_code == 200
    assert updated.json()["title"] == "Renamed"

    assert (await client.delete(f"/posts/{pid}", headers=h)).status_code == 204
    assert (await client.get(f"/posts/{pid}", headers=h)).status_code == 404


async def test_admin_can_access_any_post(client, make_author, auth_header) -> None:
    a = await make_author(email="a@x.io")
    admin = await make_author(email="admin@x.io", role=Role.admin)
    post = await _create_post(client, auth_header(a))

    resp = await client.get(f"/posts/{post['id']}", headers=auth_header(admin))

    assert resp.status_code == 200
    assert resp.json()["id"] == post["id"]


async def test_publish_sets_status_and_timestamp(
    client, make_author, auth_header
) -> None:
    a = await make_author()
    post = await _create_post(client, auth_header(a))
    pid = post["id"]
    h = auth_header(a)

    published = await client.post(f"/posts/{pid}/publish", headers=h)
    assert published.status_code == 200
    assert published.json()["status"] == "published"
    assert published.json()["published_at"] is not None

    unpublished = await client.post(f"/posts/{pid}/unpublish", headers=h)
    assert unpublished.json()["status"] == "draft"


async def test_duplicate_title_gets_unique_slug(client, make_author, auth_header) -> None:
    a = await make_author()
    h = auth_header(a)
    p1 = await _create_post(client, h, title="Same Title")
    p2 = await _create_post(client, h, title="Same Title")
    assert p1["slug"] == "same-title"
    assert p2["slug"] == "same-title-2"
