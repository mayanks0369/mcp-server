from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from app.services.keyword_extractor import extract_keywords
import time

router = APIRouter()

class KeywordOptions(BaseModel):
    topN: Optional[int] = 10

class KeywordRequest(BaseModel):
    text: str
    options: Optional[KeywordOptions] = KeywordOptions()

@router.post("/keywords")
async def extract_keywords_route(request: Request, body: KeywordRequest):
    request_id = request.state.request_id
    start = time.time()

    if len(body.text.encode("utf-8")) > 10 * 1024 * 1024:
        return {
            "requestId": request_id,
            "tool": "ExtractKeywords",
            "durationMs": 0,
            "error": {"code": "PayloadTooLarge", "message": "Text exceeds 10MB limit"}
        }

    try:
        keywords = extract_keywords(body.text, top_n=body.options.topN)
        duration = int((time.time() - start) * 1000)
        return {
            "requestId": request_id,
            "tool": "ExtractKeywords",
            "durationMs": duration,
            "result": {
                "keywords": [{"term": term, "score": float(score)} for term, score in keywords]
            }
        }
    except Exception as e:
        return {
            "requestId": request_id,
            "tool": "ExtractKeywords",
            "durationMs": 0,
            "error": {"code": "KeywordError", "message": str(e)}
        }
