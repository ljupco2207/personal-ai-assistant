import pytest

from unittest.mock import AsyncMock
from personal_ai_assistant.capstone.retry import retry_async

@pytest.mark.asyncio
async def test_retry_immediate_success():
    operation = AsyncMock(return_value="Success")

    result = await retry_async(
        operation,
        max_attempts=3,
        base_delay=0,
    )

    assert result == "Success"
    assert operation.await_count == 1


@pytest.mark.asyncio
async def test_retry_succeeds_after_two_failures():
    operation = AsyncMock(
        side_effect=[
            ConnectionError("Temporary failure"),
            ConnectionError("Temporary failure"),
            "Success",
        ]
    )

    result = await retry_async(
        operation,
        max_attempts=3,
        base_delay=0,
    )

    assert result == "Success"
    assert operation.await_count == 3


@pytest.mark.asyncio
async def test_retry_exhaustion():
    operation = AsyncMock(
        side_effect=ConnectionError("Service unavailable")
    )

    with pytest.raises(
        ConnectionError,
        match="Service unavailable",
    ):
        await retry_async(
            operation,
            max_attempts=3,
            base_delay=0,
        )

    assert operation.await_count == 3


@pytest.mark.asyncio
async def test_non_retryable_error():
    operation = AsyncMock(
        side_effect=ValueError("Invalid request")
    )

    with pytest.raises(
        ValueError,
        match="Invalid request",
    ):
        await retry_async(
            operation,
            max_attempts=3,
            base_delay=0,
        )

    # The operation must NOT be retried
    assert operation.await_count == 1

