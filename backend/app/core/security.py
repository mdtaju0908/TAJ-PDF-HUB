import time
from collections import deque
from typing import Deque, Dict, Optional
from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader

from app.core.config import settings

# API Key header dependency
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key_dependency(api_key: Optional[str] = Depends(api_key_header)):
    # Validates API key header if keys are configured; allows empty if none configured
    if settings.API_KEYS:
        if not api_key or api_key not in settings.API_KEYS:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True


class SlidingWindowRateLimiter:
    # Simple in-memory sliding window rate limiter keyed by client identifier
    def __init__(self, max_requests_per_minute: int):
        self.max = max_requests_per_minute
        self.window: Dict[str, Deque[float]] = {}

    def allow(self, client_id: str) -> bool:
        now = time.time()
        cutoff = now - 60.0
        q = self.window.setdefault(client_id, deque())
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= self.max:
            return False
        q.append(now)
        return True


rate_limiter = SlidingWindowRateLimiter(settings.RATE_LIMIT_REQUESTS_PER_MINUTE)


def get_client_id(request: Request) -> str:
    # Uses API key if present, otherwise client IP address
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"key:{api_key}"
    client_host = request.client.host if request.client else "unknown"
    return f"ip:{client_host}"


async def rate_limit_dependency(request: Request):
    client_id = get_client_id(request)
    if not rate_limiter.allow(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return True


def get_rate_limiter():
    # Returns dependency for router inclusion
    return Depends(rate_limit_dependency)

