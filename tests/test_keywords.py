import pytest

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "my-secret-api-key"
}

@pytest.mark.asyncio
async def test_keywords_success(test_client):
    payload = {
        "text": "Transformers like BERT and GPT have revolutionized NLP.",
        "options": {"topN": 3}
    }
    response = await test_client.post("/v1/keywords", headers=headers, json=payload)
    assert response.status_code == 200
    assert "keywords" in response.json()["result"]

@pytest.mark.asyncio
async def test_keywords_large_payload(test_client):
    payload = {"text": "a" * (11 * 1024 * 1024)}
    response = await test_client.post("/v1/keywords", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["error"]["code"] == "PayloadTooLarge"
