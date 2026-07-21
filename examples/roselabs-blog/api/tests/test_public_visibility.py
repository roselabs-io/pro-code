import logging

import pytest


async def _publish(client, headers, title, content="<p>body</p>") -> str:
    created = await client.post(
        "/posts", json={"title": title, "content_html": content}, headers=headers
    )
    post = created.json()
    await client.post(f"/posts/{post['id']}/publish", headers=headers)
    return post["slug"]


async def _draft(client, headers, title, content="<p>secret</p>") -> str:
    created = await client.post(
        "/posts", json={"title": title, "content_html": content}, headers=headers
    )
    return created.json()["slug"]


async def test_public_list_shows_only_published(client, make_author, auth_header) -> None:
    author = await make_author()
    h = auth_header(author)
    published_slug = await _publish(client, h, "Published One")
    draft_slug = await _draft(client, h, "Secret Draft", content="<p>do-not-leak</p>")

    resp = await client.get("/public/posts")

    assert resp.status_code == 200
    slugs = [item["slug"] for item in resp.json()["items"]]
    assert published_slug in slugs
    assert draft_slug not in slugs
    # No draft datum leaks anywhere in the payload — title or body.
    assert "Secret Draft" not in resp.text
    assert "do-not-leak" not in resp.text


async def test_public_get_published_returns_content(
    client, make_author, auth_header
) -> None:
    author = await make_author()
    slug = await _publish(
        client, auth_header(author), "Readable", content="<p>hello world</p>"
    )

    resp = await client.get(f"/public/posts/{slug}")

    assert resp.status_code == 200
    body = resp.json()
    assert body["content_html"] == "<p>hello world</p>"
    assert body["author_name"] == author.display_name


async def test_public_draft_slug_is_404_and_audited(
    client, make_author, auth_header, caplog
) -> None:
    author = await make_author()
    draft_slug = await _draft(client, auth_header(author), "Hidden")

    with caplog.at_level(logging.INFO, logger="blog"):
        resp = await client.get(f"/public/posts/{draft_slug}")

    assert resp.status_code == 404
    assert "DRAFT_ACCESS_DENIED" in caplog.text


async def test_unknown_slug_is_404(client) -> None:
    resp = await client.get("/public/posts/does-not-exist")
    assert resp.status_code == 404


# Adversarial probe — the manual stand-in for the N-vote refutation on the core
# promise: a draft must not surface through ANY public path (slug, list, pagination).
@pytest.mark.parametrize("title", ["Draft A", "Draft B", "Draft C"])
async def test_no_draft_leaks_under_probing(
    client, make_author, auth_header, title
) -> None:
    author = await make_author()
    h = auth_header(author)
    draft_slug = await _draft(client, h, title, content=f"<p>leak-{title}</p>")

    assert (await client.get(f"/public/posts/{draft_slug}")).status_code == 404

    listed = await client.get("/public/posts?limit=50")
    assert draft_slug not in [item["slug"] for item in listed.json()["items"]]
    assert title not in listed.text
    assert f"leak-{title}" not in listed.text
