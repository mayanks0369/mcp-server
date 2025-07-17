from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import uuid
import time

from app.routes import summarize, keywords, sentiment
from app.utils.logger import log_request

app = FastAPI(
    title="MCP Server",
    version="1.0",
    description="Model Context Protocol API for NLP tasks"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, replace "*" with specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # must include "X-Api-Key"
)

API_KEY = "my-secret-api-key"  # move to env in production


@app.middleware("http")
async def add_request_id_and_logging(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "requestId": request_id,
                "error": {"code": "InternalError", "message": str(e)}
            }
        )

    duration = int((time.time() - start_time) * 1000)
    log_request(request, response.status_code, duration)
    return response


@app.middleware("http")
async def check_api_key(request: Request, call_next):
    # Allow unauthenticated access to Swagger docs, schema, and frontend
    public_exact_paths = ["/", "/openapi.json", "/favicon.ico"]
    public_prefixes = ["/docs", "/redoc", "/static"]

    if request.url.path in public_exact_paths or any(request.url.path.startswith(p) for p in public_prefixes):
        return await call_next(request)

    # Require API key for all other routes
    api_key = request.headers.get("X-Api-Key")
    if api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "requestId": str(uuid.uuid4()),
                "error": {"code": "Unauthorized", "message": "Invalid API Key"},
            },
        )
    return await call_next(request)



@app.get("/health")
async def health():
    return {"status": "ok", "version": app.version}


from fastapi.responses import FileResponse

@app.get("/")
async def serve_ui():
    return FileResponse("static/index.html")


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Include NLP task routes
app.include_router(summarize.router, prefix="/v1")
app.include_router(keywords.router, prefix="/v1")
app.include_router(sentiment.router, prefix="/v1")
