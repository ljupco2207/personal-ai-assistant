import pytest
from pydantic import ValidationError

from personal_ai_assistant.capstone.structured_models import (
    IntentResult,
)


def test_valid_intent_result():
    result = IntentResult.model_validate_json(
        """
        {
            "intent": "reminder",
            "task": "call John",
            "date": "tomorrow"
        }
        """
    )

    assert result.intent == "reminder"
    assert result.task == "call John"
    assert result.date == "tomorrow"


def test_invalid_intent():
    with pytest.raises(ValidationError):
        IntentResult.model_validate_json(
            """
            {
                "intent": "shopping",
                "task": "buy milk",
                "date": "tomorrow"
            }
            """
        )


def test_invalid_date_type():
    with pytest.raises(ValidationError):
        IntentResult.model_validate_json(
            """
            {
                "intent": "reminder",
                "task": "call John",
                "date": 123
            }
            """
        )


def test_missing_required_field():
    with pytest.raises(ValidationError):
        IntentResult.model_validate_json(
            """
            {
                "intent": "reminder",
                "date": "tomorrow"
            }
            """
        )


def test_null_date():
    result = IntentResult.model_validate_json(
        """
        {
            "intent": "general",
            "task": "explain Python decorators",
            "date": null
        }
        """
    )

    assert result.date is None

def test_extra_field_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        IntentResult.model_validate_json(
            """
            {
                "intent": "reminder",
                "task": "call John",
                "date": "tomorrow",
                "priority": "high"
            }
            """
        )
    assert exc_info.value.errors()[0]["type"] == "extra_forbidden"