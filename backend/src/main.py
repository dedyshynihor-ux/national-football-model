import logging
import time
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from jokes.router import router as jokes_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("joke_generator.audit")
REQUESTS_PER_MINUTE = 60
requests: dict[str, deque[float]] = defaultdict(deque)

app = FastAPI(title="Joke Generator API", version="1.0.0")
app.include_router(jokes_router)


@app.middleware("http")
async def audit_and_rate_limit(request: Request, call_next):
    client = request.client.host if request.client else "unknown"
    now = time.monotonic()
    for known_client, known_requests in list(requests.items()):
        while known_requests and known_requests[0] <= now - 60:
            known_requests.popleft()
        if not known_requests:
            del requests[known_client]
    client_requests = requests[client]
    if len(client_requests) >= REQUESTS_PER_MINUTE:
        logger.warning("Rate limited request: %s %s from %s", request.method, request.url.path, client)
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    client_requests.append(now)
    response = await call_next(request)
    logger.info("%s %s %s from %s", request.method, request.url.path, response.status_code, client)
    return response
