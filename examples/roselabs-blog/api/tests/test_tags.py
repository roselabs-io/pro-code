async def _publish(client, headers, title, tags):
    created = await client.post(
        "/posts",
        json={"title": title, "content_html": "<p>x</p>", "tags": tags},
        headers=headers,
    )
    await client.post(f"/posts/{created.json()['id']}/publish", headers=headers)
    return created.json()["slug"]


async def test_create_post_with_tags(client, make_author, auth_header) -> None:
    author = await make_author()
    resp = await client.post(
        "/posts",
        json={"title": "Tagged", "content_html": "<p>x</p>", "tags": ["AI", "Control"]},
        headers=auth_header(author),
    )
    assert resp.status_code == 201
    assert sorted(resp.json()["tags"]) == ["AI", "Control"]


async def test_public_filter_by_tag(client, make_author, auth_header) -> None:
    author = await make_author()
    h = auth_header(author)
    ai_slug = await _publish(client, h, "On AI", ["ai"])
    food_slug = await _publish(client, h, "On Cooking", ["food"])

    resp = await client.get("/public/posts?tag=ai")

    slugs = [item["slug"] for item in resp.json()["items"]]
    assert ai_slug in slugs
    assert food_slug not in slugs


async def test_public_detail_includes_tags(client, make_author, auth_header) -> None:
    author = await make_author()
    h = auth_header(author)
    slug = await _publish(client, h, "With Tags", ["ai", "ml"])

    detail = await client.get(f"/public/posts/{slug}")

    assert sorted(detail.json()["tags"]) == ["ai", "ml"]


async def test_update_replaces_tags(client, make_author, auth_header) -> None:
    author = await make_author()
    h = auth_header(author)
    created = await client.post(
        "/posts",
        json={"title": "T", "content_html": "<p>x</p>", "tags": ["a"]},
        headers=h,
    )
    updated = await client.patch(
        f"/posts/{created.json()['id']}", json={"tags": ["b", "c"]}, headers=h
    )
    assert sorted(updated.json()["tags"]) == ["b", "c"]


async def test_tag_slug_is_normalized_and_reused(
    client, make_author, auth_header
) -> None:
    author = await make_author()
    h = auth_header(author)
    first = await _publish(client, h, "One", ["AI"])
    second = await _publish(client, h, "Two", ["ai"])

    resp = await client.get("/public/posts?tag=AI")

    slugs = [item["slug"] for item in resp.json()["items"]]
    assert first in slugs
    assert second in slugs
