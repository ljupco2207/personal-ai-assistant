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
from pydantic import ValidationError
from personal_ai_assistant.capstone.structured_models import (
    IntentResult,
)
from personal_ai_assistant.capstone.json_utils import (
    strip_json_code_fence,
)


async def main():
    load_dotenv()

    client = AsyncAnthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        max_retries=2,
    )

    provider = AnthropicProvider(client=client)

    system_prompt = """
You are an intent classifier.

Classify the user's message into:
calendar, reminder, general.

Return only a valid JSON object with:
- intent: one of the allowed categories
- task: the action requested by the user
- date: the date expression, or null if absent

Do not include Markdown or explanations.
"""

    messages = [
        Message(
            role=Role.SYSTEM,
            content=system_prompt,
        ),
        Message(
            role=Role.USER,
            content="Remind me to call John tomorrow.",
        ),
    ]

    response = await provider.generate(messages)

    try:
        cleaned_json = strip_json_code_fence(
            response.message.content
        )

        result = IntentResult.model_validate_json(
            cleaned_json
        )

        print("Validated intent:", result.intent)
        print("Task:", result.task)
        print("Date:", result.date)

    except ValidationError as error:
        print("Claude returned invalid structured data:")
        print(error)

    print("Claude response:")
    print(response.message.content)


if __name__ == "__main__":
    asyncio.run(main())