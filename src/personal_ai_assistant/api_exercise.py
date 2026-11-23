import httpx
import asyncio

from dataclasses import dataclass
from personal_ai_assistant.config import load_config

@dataclass
class Post:
    userId: int
    id: int
    title: str
    body: str

    def summary(self) -> str:
        return f"Post #{self.id}: {self.title}"

def parse_post(data: object) -> Post:
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")

    if type(data.get("userId")) is not int:
        raise ValueError("Invalid userId")

    if type(data.get("id")) is not int:
        raise ValueError("Invalid id")

    if not isinstance(data.get("title"), str):
        raise ValueError("Invalid title")

    if not isinstance(data.get("body"), str):
        raise ValueError("Invalid body")

    return Post(**data)

async def fetch_post(
    client: httpx.AsyncClient,
    post_id: int
) -> Post | None:
    try:
        response = await client.get(
            f"https://jsonplaceholder.typicode.com/posts/{post_id}"
        )

        response.raise_for_status()
        data = response.json()
        return parse_post(data)
    except httpx.HTTPStatusError as error:
        status = error.response.status_code

        if status == 404:
            print(f"Post #{post_id} not found")
        elif status >= 500:
            print(f"Server error: {status}")
        else:
            print(f"HTTP error: {status}")

        return None
    except httpx.RequestError as error:
        print(f"Network error: {error}")
        return None
    except ValueError as error:
        print(f"Invalid API response: {error}")
        return None


async def main() -> None:

    config = load_config()

    print(f"Environment: {config.environment}")
    print(f"Timeout: {config.timeout}")
    print(f"API key configured: {bool(config.api_key)}")

    async with httpx.AsyncClient(timeout=config.timeout) as client:
        posts = await asyncio.gather(
            fetch_post(client, 1),
            fetch_post(client, 2),
            fetch_post(client, 999999),
            fetch_post(client, 4),
            fetch_post(client, 5)
        )

        for post in posts:
            if post is not None:
                print(post.summary())
            else:
                print("Failed to fetch post")


if __name__ == "__main__":
    asyncio.run(main())
