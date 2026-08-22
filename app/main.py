import redis
import os
from fastapi import FastAPI
from fastapi import HTTPException
from app.limiter import is_allowed
from pydantic import BaseModel
from metrics import allowed_count, rejected_count
from prometheus_client import make_asgi_app
from app.producer import emit_event

class RateLimitRequest(BaseModel):
    client_id: str
    limit: int
    window_seconds: int

app = FastAPI()
redis_client = redis.asyncio.Redis(host='redis', port=6379, decode_responses=True)

metrics_app = make_asgi_app()
app.mount("/metrics/", metrics_app)

@app.post("/check")

async def request(request: RateLimitRequest):
    result = await is_allowed(redis_client, request.client_id, request.limit, request.window_seconds)
    if result: 
        allowed_count.labels(client_id=request.client_id).inc()
        emit_event(request.client_id, True, request.limit, request.window_seconds)
    else:
        rejected_count.labels(client_id=request.client_id).inc()
        emit_event(request.client_id, False, request.limit, request.window_seconds)
        raise HTTPException(status_code=429, detail="Too many requests")

    return {"allowed": True, "message": "Request allowed", "instance": os.getenv("HOSTNAME")}        
