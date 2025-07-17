import pytest

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "my-secret-api-key"
}

@pytest.mark.asyncio
async def test_summarize_success(test_client):
    payload = {
        "text": "AI is transforming industries by enabling machines to learn from data. This leads to better automation, personalization, and decision-making.",
        "options": {"maxSentences": 2}
    }
    response = await test_client.post("/v1/summarize", headers=headers, json=payload)
    assert response.status_code == 200
    assert "summary" in response.json()["result"]

@pytest.mark.asyncio
async def test_summarize_invalid_json(test_client):
    response = await test_client.post("/v1/summarize", headers=headers, content="notjson")
    assert response.status_code == 422  # FastAPI auto-handles this

@pytest.mark.asyncio
async def test_summarize_missing_key(test_client):
    payload = {"options": {"maxSentences": 2}}
    response = await test_client.post("/v1/summarize", headers=headers, json=payload)
    assert response.status_code == 422
