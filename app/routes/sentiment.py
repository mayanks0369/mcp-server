from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.services.sentiment_analyzer import analyze_sentiment
import time

router = APIRouter()

class SentimentRequest(BaseModel):
    text: str

@router.post("/sentiment")
async def sentiment_route(request: Request, body: SentimentRequest):
    request_id = request.state.request_id
    start = time.time()

    if len(body.text.encode("utf-8")) > 10 * 1024 * 1024:
        return {
            "requestId": request_id,
            "tool": "Sentiment",
            "durationMs": 0,
            "error": {"code": "PayloadTooLarge", "message": "Text exceeds 10MB limit"}
        }

    try:
        label, score = analyze_sentiment(body.text)
        duration = int((time.time() - start) * 1000)
        return {
            "requestId": request_id,
            "tool": "Sentiment",
            "durationMs": duration,
            "result": {
                "label": label,
                "confidence": round(score, 4)
            }
        }
    except Exception as e:
        return {
            "requestId": request_id,
            "tool": "Sentiment",
            "durationMs": 0,
            "error": {"code": "SentimentError", "message": str(e)}
        }
