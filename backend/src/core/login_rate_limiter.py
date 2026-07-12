from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, status


class LoginRateLimiter:
    def __init__(self, max_attempts: int = 5, window_seconds: int = 300) -> None:
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()
        self._next_cleanup = monotonic() + window_seconds

    def check(self, key: str) -> None:
        now = monotonic()
        with self._lock:
            self._cleanup(now)
            attempts = self._active_attempts(key, now)
            if len(attempts) >= self.max_attempts:
                retry_after = max(1, int(self.window_seconds - (now - attempts[0])))
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many login attempts. Try again later.",
                    headers={"Retry-After": str(retry_after)},
                )

    def record_failure(self, key: str) -> None:
        now = monotonic()
        with self._lock:
            self._cleanup(now)
            self._active_attempts(key, now).append(now)

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._attempts.clear()
                self._next_cleanup = monotonic() + self.window_seconds
            else:
                self._attempts.pop(key, None)

    def _active_attempts(self, key: str, now: float) -> deque[float]:
        attempts = self._attempts[key]
        cutoff = now - self.window_seconds
        while attempts and attempts[0] <= cutoff:
            attempts.popleft()
        return attempts

    def _cleanup(self, now: float) -> None:
        if now < self._next_cleanup:
            return
        for key in list(self._attempts):
            if not self._active_attempts(key, now):
                self._attempts.pop(key, None)
        self._next_cleanup = now + self.window_seconds


login_rate_limiter = LoginRateLimiter()
