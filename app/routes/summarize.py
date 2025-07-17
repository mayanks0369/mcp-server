from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from app.services.summarizer import summarize_text
from uuid import uuid4
import time

router = APIRouter()

class SummarizeOptions(BaseModel):
    maxSentences: Optional[int] = 3

class SummarizeRequest(BaseModel):
    text: str
    options: Optional[SummarizeOptions] = SummarizeOptions()

@router.post("/summarize")
async def summarize(request: Request, body: SummarizeRequest):
    request_id = request.state.request_id
    start = time.time()

    if len(body.text.encode("utf-8")) > 10 * 1024 * 1024:
        return {
            "requestId": request_id,
            "tool": "Summarize",
            "durationMs": 0,
            "error": {"code": "PayloadTooLarge", "message": "Text exceeds 10MB limit"}
        }

    try:
        result = summarize_text(body.text, body.options.maxSentences)
        duration = int((time.time() - start) * 1000)
        return {
            "requestId": request_id,
            "tool": "Summarize",
            "durationMs": duration,
            "result": {"summary": result}
        }
    except Exception as e:
        return {
            "requestId": request_id,
            "tool": "Summarize",
            "durationMs": 0,
            "error": {"code": "SummarizeError", "message": str(e)}
        }
