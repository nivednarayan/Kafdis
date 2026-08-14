import redis
from fastapi import FastAPI
from fastapi import HTTPException
from app.limiter import is_allowed
from pydantic import BaseModel

class RateLimitRequest(BaseModel):
    client_id: str
    limit: int
    window_seconds: int

app = FastAPI()
redis_client = redis.asyncio.Redis(host='redis', port=6379, decode_responses=True)

@app.post("/check")

async def request(request: RateLimitRequest):
    result = await is_allowed(redis_client, request.client_id, request.limit, request.window_seconds)
    if not result:
        raise HTTPException(status_code=429, detail="Too many requests")

    return {"allowed": True, "message": "Request allowed"}        
