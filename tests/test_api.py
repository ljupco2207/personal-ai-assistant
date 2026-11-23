import pytest
import httpx

from personal_ai_assistant.api_exercise import Post, parse_post, fetch_post
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def sample_post() -> Post:
    return Post(
        userId=1,
        id=10,
        title="Hello",
        body="Body"
    )

def test_post_id(sample_post: Post):
    assert sample_post.id == 10


def test_post_summary(sample_post: Post):
    assert sample_post.summary() == "Post #10: Hello"

def test_parse_post_with_valid_data():
    # Arrange
    data = {
        "userId": 1,
        "id": 10,
        "title": "Learning pytest",
        "body": "Testing Python applications"
    }

    # Act
    post = parse_post(data)

    # Assert
    assert isinstance(post, Post)
    assert post.id == 10
    assert post.title == "Learning pytest"

def test_parse_post_with_invalid_user_id():
    # Arrange
    data = {
        "userId": "invalid",
        "id": 10,
        "title": "Learning pytest",
        "body": "Testing Python applications"
    }

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid userId"):
        parse_post(data)


@pytest.mark.parametrize(
    "field, invalid_value, expected_error",
    [
        ("userId", "invalid", "Invalid userId"),
        ("userId", True, "Invalid userId"),
        ("id", None, "Invalid id"),
        ("title", 123, "Invalid title"),
        ("title", None, "Invalid title"),
        ("body", None, "Invalid body"),
    ]
)

def test_parse_post_with_invalid_fields(
    field: str,
    invalid_value: object,
    expected_error: str
):
    # Arrange
    data = {
        "userId": 1,
        "id": 10,
        "title": "Learning pytest",
        "body": "Testing Python applications"
    }

    data[field] = invalid_value

    # Act & Assert
    with pytest.raises(ValueError, match=expected_error):
        parse_post(data)


@pytest.mark.asyncio
async def test_fetch_post_success():
    # Arrange
    mock_client = Mock()
    mock_client.get = AsyncMock()

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "userId": 1,
        "id": 10,
        "title": "Mocked Post",
        "body": "Testing without internet"
    }

    mock_client.get.return_value = mock_response

    # Act
    post = await fetch_post(mock_client, 10)

    # Assert
    assert post is not None
    assert post.id == 10
    assert post.title == "Mocked Post"

    mock_client.get.assert_awaited_once_with(
        "https://jsonplaceholder.typicode.com/posts/10"
    )

    mock_response.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_fetch_post_not_found():
    # Arrange
    mock_client = Mock()
    mock_client.get = AsyncMock()

    request = httpx.Request(
        "GET",
        "https://jsonplaceholder.typicode.com/posts/999999"
    )

    response = httpx.Response(
        status_code=404,
        request=request
    )

    mock_client.get.return_value = response

    # Act
    post = await fetch_post(mock_client, 999999)

    # Assert
    assert post is None

    mock_client.get.assert_awaited_once_with(
        "https://jsonplaceholder.typicode.com/posts/999999"
    )

@pytest.mark.asyncio
async def test_fetch_post_server_error():
    mock_client = Mock()
    mock_client.get = AsyncMock()

    request = httpx.Request(
        "GET",
        "https://jsonplaceholder.typicode.com/posts/10"
    )

    response = httpx.Response(
        status_code=500,
        request=request
    )

    mock_client.get.return_value = response

        # Act
    post = await fetch_post(mock_client, 10)

    # Assert
    assert post is None

    mock_client.get.assert_awaited_once_with(
        "https://jsonplaceholder.typicode.com/posts/10"
    )

@pytest.mark.asyncio
async def test_fetch_post_timeout():
    mock_client = Mock()
    mock_client.get = AsyncMock(
        side_effect=httpx.TimeoutException(
            "Request timed out"
        )
    )

    post = await fetch_post(mock_client, 10)

    assert post is None

