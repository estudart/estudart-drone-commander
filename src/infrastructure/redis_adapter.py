from collections.abc import Iterator

import redis


class RedisAdapter:
    """
    Thin wrapper around redis-py for pub/sub. Inject this class where Redis is needed.

    ``decode_responses=True`` yields str payloads instead of bytes.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        *,
        decode_responses: bool = True,
    ):
        self._client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    def publish(self, channel: str, message: str) -> int:
        """Publish ``message`` to ``channel``. Returns subscriber count that received it."""
        return int(self._client.publish(channel, message))

    def consume(self, channel: str) -> Iterator[str]:
        """
        Subscribe to ``channel`` and yield each message body (blocking generator).

        Skips non-data frames (e.g. subscribe confirmations). Runs until the
        generator is closed or the client disconnects.
        """
        pubsub = self._client.pubsub()
        pubsub.subscribe(channel)
        try:
            for raw in pubsub.listen():
                if raw.get("type") == "message":
                    yield raw["data"]
        finally:
            try:
                pubsub.close()
            except redis.RedisError:
                pass

    def close(self) -> None:
        """Close the underlying Redis connection pool."""
        self._client.close()
