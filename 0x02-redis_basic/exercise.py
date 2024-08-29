#!/usr/bin/env python3
""" Exercise module. """
import redis
import uuid


class Cache:
    def __init__(self):
        """
        Instantiates a new Cache object.

        This object uses the redis client to interact with Redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str) -> str:
        """
        Stores given data in Redis and returns its key.

        Args:
            data: The data to be stored.

        Returns:
            The key at which the data is stored.
        """
        key = uuid.uuid4().hex
        self._redis.set(key, data)

        return key
