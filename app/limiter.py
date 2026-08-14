limiter = """
local now = ARGV[1]
local limit = ARGV[2]
local member = ARGV[3]
local window_ms = ARGV[4]
local ttl = ARGV[5]

local cutoff = tonumber(now) - tonumber(window_ms)

redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, cutoff)
local count = redis.call('ZCARD', KEYS[1])

if count >= tonumber(limit) then
    return 0
end

redis.call('ZADD', KEYS[1], tonumber(now), member)
redis.call('EXPIRE', KEYS[1], ttl)

return 1
"""

import time
import uuid

async def is_allowed(redis_client, client_id, limit, window_seconds):
    arg1 = int(time.time() * 1000);
    arg2 = limit
    arg3 = str(uuid.uuid4())
    arg4 = window_seconds * 1000
    arg5 = window_seconds
    result = await redis_client.eval(limiter, 1, f"rate_limit:{client_id}", arg1, arg2, arg3, arg4, arg5)
    return result == 1
