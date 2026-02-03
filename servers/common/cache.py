"""Caching utilities for MCP servers."""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
import hashlib


class Cache:
    """Simple file-based cache with TTL support."""

    def __init__(self, cache_dir: str, ttl_seconds: int = 3600):
        """
        Initialize cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time to live in seconds (default: 1 hour)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self.enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"

    def _get_cache_key(self, key: str) -> str:
        """Generate cache file path from key."""
        # Use hash to avoid filesystem issues with long/special characters
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return str(self.cache_dir / f"{key_hash}.json")

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if not self.enabled:
            return None

        cache_file = self._get_cache_key(key)

        if not os.path.exists(cache_file):
            return None

        try:
            with open(cache_file, "r") as f:
                data = json.load(f)

            # Check if expired
            cached_time = datetime.fromisoformat(data["timestamp"])
            if datetime.now() - cached_time > timedelta(seconds=self.ttl_seconds):
                # Cache expired, remove file
                os.remove(cache_file)
                return None

            return data["value"]
        except (json.JSONDecodeError, KeyError, ValueError, OSError):
            # Invalid cache file, remove it
            try:
                os.remove(cache_file)
            except OSError:
                pass
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
        """
        if not self.enabled:
            return

        cache_file = self._get_cache_key(key)

        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "key": key,  # Store original key for debugging
                "value": value,
            }

            with open(cache_file, "w") as f:
                json.dump(data, f, indent=2)
        except (TypeError, OSError) as e:
            # If caching fails, just continue without cache
            pass

    def invalidate(self, key: str) -> None:
        """
        Invalidate cache entry.

        Args:
            key: Cache key
        """
        cache_file = self._get_cache_key(key)
        try:
            if os.path.exists(cache_file):
                os.remove(cache_file)
        except OSError:
            pass

    def clear(self) -> None:
        """Clear all cache entries."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
        except OSError:
            pass

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        removed = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, "r") as f:
                        data = json.load(f)

                    cached_time = datetime.fromisoformat(data["timestamp"])
                    if datetime.now() - cached_time > timedelta(seconds=self.ttl_seconds):
                        cache_file.unlink()
                        removed += 1
                except (json.JSONDecodeError, KeyError, ValueError, OSError):
                    # Invalid cache file, remove it
                    cache_file.unlink()
                    removed += 1
        except OSError:
            pass

        return removed
