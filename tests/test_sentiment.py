import pytest

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "my-secret-api-key"
}

@pytest.mark.asyncio
async def test_sentiment_positive(test_client):
    payload = {"text": "I love this product! It's amazing!"}
    response = await test_client.post("/v1/sentiment", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["result"]["label"] == "positive"

@pytest.mark.asyncio
async def test_sentiment_unauthorized(test_client):
    payload = {"text": "This is okay."}
    response = await test_client.post("/v1/sentiment", headers={
        "Content-Type": "application/json"
    }, json=payload)
    assert response.status_code == 401
