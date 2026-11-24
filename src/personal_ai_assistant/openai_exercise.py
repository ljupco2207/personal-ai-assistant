import asyncio

from openai import AsyncOpenAI
from personal_ai_assistant.config import load_config


async def main() -> None:
    config = load_config()

    client = AsyncOpenAI(
        api_key=config.api_key,
        timeout=config.timeout,
    )

    response = await client.responses.create(
        model="gpt-4.1-mini",
        input="Explain Python async/await in two sentences.",
    )

    print(response.output_text)


if __name__ == "__main__":
    asyncio.run(main())