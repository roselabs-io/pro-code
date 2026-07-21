import xml.etree.ElementTree as ET


async def test_rss_lists_published_only(client, make_author, auth_header) -> None:
    author = await make_author()
    h = auth_header(author)
    created = await client.post(
        "/posts", json={"title": "RSS Post", "content_html": "<p>x</p>"}, headers=h
    )
    await client.post(f"/posts/{created.json()['id']}/publish", headers=h)
    await client.post(
        "/posts", json={"title": "Draft Post", "content_html": "<p>x</p>"}, headers=h
    )

    resp = await client.get("/rss")

    assert resp.status_code == 200
    assert "application/rss+xml" in resp.headers["content-type"]
    assert "RSS Post" in resp.text
    assert "Draft Post" not in resp.text
    ET.fromstring(resp.text)  # parses as valid XML
