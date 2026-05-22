# backend/memory.py

import os
import json
import time

try:
    import redis
except Exception:
    redis = None

REDIS_URL = os.getenv("REDIS_URL", None)


class Memory:
    def __init__(self):
        if redis and REDIS_URL:
            self._client = redis.from_url(REDIS_URL)
            print("Using Redis for memory")
        else:
            self._client = None
            self._store = {}
            print("Using in-memory store (dev mode)")

    # -------------------------
    # LOW LEVEL
    # -------------------------
    def _set(self, key: str, value: dict, ttl: int = None):
        payload = json.dumps(value)

        if self._client:
            if ttl:
                self._client.setex(key, ttl, payload)
            else:
                self._client.set(key, payload)
        else:
            expiry = time.time() + ttl if ttl else None
            self._store[key] = (expiry, payload)

    def _get(self, key: str) -> dict:
        if self._client:
            v = self._client.get(key)
            return json.loads(v) if v else None
        else:
            v = self._store.get(key)
            if not v:
                return None

            expiry, payload = v

            if expiry and time.time() > expiry:
                del self._store[key]
                return None

            return json.loads(payload)

    def delete(self, key: str):
        if self._client:
            self._client.delete(key)
        else:
            if key in self._store:
                del self._store[key]

    # -------------------------
    # HIGH LEVEL (IMPORTANT)
    # -------------------------

    def get_session(self, session_id: str):
        return self._get(f"session:{session_id}") or {}

    def update_session(self, session_id: str, data: dict, ttl: int = 900):
        session = self.get_session(session_id)
        session.update(data)
        self._set(f"session:{session_id}", session, ttl)

    def clear_session(self, session_id: str):
        self.delete(f"session:{session_id}")

    # -------------------------
    # USER MEMORY (LONG TERM)
    # -------------------------

    def get_user(self, user_id: str):
        return self._get(f"user:{user_id}") or {}

    def update_user(self, user_id: str, data: dict):
        user = self.get_user(user_id)
        user.update(data)
        self._set(f"user:{user_id}", user)

# Global instance
memory = Memory()