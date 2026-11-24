import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def retry_async(
    operation: Callable[[], Awaitable[T]],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    retryable_exceptions: tuple[type[Exception], ...] = (
        ConnectionError,
        TimeoutError,
    ),
) -> T:
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    if base_delay < 0:
        raise ValueError("base_delay must be >= 0")

    for attempt in range(max_attempts):
        try:
            return await operation()

        except retryable_exceptions:
            if attempt == max_attempts - 1:
                raise

            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)

    raise RuntimeError("Unreachable")
