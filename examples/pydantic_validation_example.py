from pydantic import ValidationError

from personal_ai_assistant.capstone.structured_models import (
    IntentResult,
)


claude_response = """
{
    "intent": "reminder",
    "task": "call John",
    "date": "tomorrow"
}
"""

try:
    result = IntentResult.model_validate_json(claude_response)

    print("Intent:", result.intent)
    print("Task:", result.task)
    print("Date:", result.date)

except ValidationError as error:
    print("Validation failed:")
    print(error)