import asyncio
import os

from dotenv import load_dotenv
from anthropic import AsyncAnthropic

from personal_ai_assistant.capstone.anthropic_provider import (
    AnthropicProvider,
)
from personal_ai_assistant.capstone.intent_prompts import (
    INTENT_CLASSIFICATION_PROMPT,
)
from personal_ai_assistant.capstone.models import (
    Message,
    Role,
)


async def main():
    load_dotenv()

    client = AsyncAnthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        max_retries=2,
    )

    provider = AnthropicProvider(client=client)

    prompt = INTENT_CLASSIFICATION_PROMPT.render(
        user_message="Remind me to call John tomorrow."
    )

    response = await provider.generate([
        Message(
            role=Role.USER,
            content=prompt,
        )
    ])

    print("Claude classification:", response.message.content)


if __name__ == "__main__":
    asyncio.run(main())