import asyncio
import os

from anthropic import AsyncAnthropic
from dotenv import load_dotenv

from personal_ai_assistant.capstone.anthropic_provider import (
    AnthropicProvider,
)
from personal_ai_assistant.capstone.models import (
    Message,
    Role,
)
from personal_ai_assistant.capstone.service import AssistantService
from personal_ai_assistant.capstone.storage import JSONConversationStorage


async def main() -> None:
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is missing")

    async with AsyncAnthropic(
        api_key=api_key,
        max_retries=2,
        timeout=30.0,
    ) as client:

        provider = AnthropicProvider(client=client)

        storage = JSONConversationStorage(
            "data/conversation.json"
        )

        service = AssistantService(
            provider=provider,
            storage=storage,
        )

        print("Claude: ", end="", flush=True)

        async for chunk in service.stream_message(
            "Explain Python async generators in 3 sentences."
        ):
            print(chunk, end="", flush=True)

        print()



if __name__ == "__main__":
    asyncio.run(main())
