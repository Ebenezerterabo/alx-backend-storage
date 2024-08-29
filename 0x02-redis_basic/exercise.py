#!/usr/bin/env python3
""" Exercise module. """
import redis
import uuid
from typing import Callable, Union


class Cache:
    def __init__(self):
        """
        Instantiates a new Cache object.

        This object uses the redis client to interact with Redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
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

    def get(self, key: str, fn: Callable = None) -> str:
        """
        Gets data from Redis.

        Args:
            key: The key at which the data is stored.
            fn: The function to be applied to the data.

        Returns:
            The data stored at the key.
        """
        data = self._redis.get(key)

        if fn:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        """
        Gets data from Redis and converts it to a string.

        Args:
            key: The key at which the data is stored.

        Returns:
            The data stored at the key as a string.
        """
        return str(self.get(key))

    def get_int(self, key: str) -> int:
        """
        Gets data from Redis and converts it to an integer.

        Args:
            key: The key at which the data is stored.

        Returns:
            The data stored at the key as an integer.
        """
        return int(self.get(key))
