"""Shared cache for computed statistics.

Results are memoised in a Redis instance so that several processes computing
over the same data do not each recompute it. The cache is keyed on the function
name and a digest of the input values.

The server address comes from STATS_CACHE_URL. When it is unset the cache is
disabled and every lookup misses, so callers work unchanged without one.
"""

from __future__ import annotations

import hashlib
import json
import os

import redis

_CLIENT: redis.Redis | None = None


def _client() -> redis.Redis | None:
    """Return the shared Redis client, or None when no server is configured."""
    global _CLIENT
    url = os.environ.get("STATS_CACHE_URL")
    if not url:
        return None
    if _CLIENT is None:
        _CLIENT = redis.Redis.from_url(url, socket_timeout=2)
    return _CLIENT


def _key(name: str, values: list[float]) -> str:
    payload = json.dumps([name, values], separators=(",", ":"))
    return "stats:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def lookup(name: str, values: list[float], client: redis.Redis | None = None) -> float | None:
    """Return the cached result for this call, or None when it is absent."""
    conn = client or _client()
    if conn is None:
        return None
    cached = conn.get(_key(name, values))
    return None if cached is None else float(cached)


def store(name: str, values: list[float], result: float, client: redis.Redis | None = None) -> None:
    """Record *result* as the answer for this call."""
    conn = client or _client()
    if conn is None:
        return
    conn.set(_key(name, values), str(float(result)))
