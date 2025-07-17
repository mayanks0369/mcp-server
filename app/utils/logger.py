import structlog

logger = structlog.get_logger()

def log_request(request, status_code, duration_ms):
    logger.info(
        "request_log",
        method=request.method,
        path=request.url.path,
        status=status_code,
        durationMs=duration_ms
    )
