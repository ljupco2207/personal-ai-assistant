import asyncio
import os

from anthropic import AsyncAnthropic
from dotenv import load_dotenv


async def main() -> None:
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is missing")

    async with AsyncAnthropic(
        api_key=api_key,
        timeout=30.0,
    ) as client:
        response = await client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": "Explain Python async/await in two sentences.",
                }
            ],
        )

        for block in response.content:
            if block.type == "text":
                print(block.text)


if __name__ == "__main__":
    asyncio.run(main())
