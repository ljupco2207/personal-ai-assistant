import asyncio
import os

from anthropic import AsyncAnthropic
from dotenv import load_dotenv

from personal_ai_assistant.capstone.anthropic_provider import (
    AnthropicProvider,
)
from personal_ai_assistant.capstone.intent_classifier import (
    IntentClassifier,
)


async def main():
    load_dotenv()

    client = AsyncAnthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        max_retries=2,
    )

    provider = AnthropicProvider(client=client)
    classifier = IntentClassifier(provider=provider)

    messages = [
        "Remind me to call John tomorrow.",
        "Schedule a meeting with Alex on Friday.",
        "Explain how Python decorators work.",
    ]

    for message in messages:
        result = await classifier.classify(message)

        print(f"\nUser: {message}")
        print(f"Intent: {result.intent}")
        print(f"Task: {result.task}")
        print(f"Date: {result.date}")


if __name__ == "__main__":
    asyncio.run(main())