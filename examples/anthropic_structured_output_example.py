import asyncio
import os

from anthropic import AsyncAnthropic
from dotenv import load_dotenv

from personal_ai_assistant.capstone.structured_models import (
    IntentResult,
)


async def main():
    load_dotenv()

    client = AsyncAnthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
    )

    response = await client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Remind me to call John tomorrow.",
            }
        ],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": IntentResult.model_json_schema(),
            }
        },
    )

    raw_json = response.content[0].text

    result = IntentResult.model_validate_json(raw_json)

    print("Validated intent:", result.intent)
    print("Task:", result.task)
    print("Date:", result.date)


if __name__ == "__main__":
    asyncio.run(main())