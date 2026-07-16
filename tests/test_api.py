import pytest

@pytest.mark.asyncio
async def test_create_link(client):
    response = await client.post("/links", json={"original_url": "https://example.com"})
    body = response.json()
    assert response.status_code == 201
    assert "id" in body
    assert "short_code" in body
    assert "short_url" in body
    assert body["original_url"] == "https://example.com/"


@pytest.mark.asyncio
async def test_get_links(client):
    await client.post("/links", json={"original_url": "https://example.com"})

    response = await client.get("/links")
    body = response.json()
    assert response.status_code == 200
    assert isinstance(body, list)
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_redirect(client, test_link):
    short_code = test_link["short_code"]

    response = await client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["Location"] == "https://example.com/"


@pytest.mark.asyncio
async def test_delete_link(client, test_link):
    short_code = test_link["short_code"]

    response = await client.delete(f"/links/{short_code}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Link with short_code '{short_code}' deleted"
