#!/usr/bin/env python3
""" Exercise module. """
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Counts the number of calls. """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function. """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Stores the history of inputs and outputs. """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function. """
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """ Prints the history of calls. """
    name = method.__qualname__
    redis = method.__self__._redis
    # Get the list of inputs and outputs
    inputs = redis.lrange(name + ":inputs", 0, -1)
    outputs = redis.lrange(name + ":outputs", 0, -1)
    # Print total number of calls
    print("{} was called {} times:".format(name, redis.get(name)))

    # Iterate the total number of calls
    for inp, out in zip(inputs, outputs):
        inp_decoded = inp.decode("utf-8")
        out_decoded = out.decode("utf-8")
        print("{}(*{}) -> {}".format(name, inp_decoded, out_decoded))


class Cache:
    def __init__(self):
        """
        Instantiates a new Cache object.

        This object uses the redis client to interact with Redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
