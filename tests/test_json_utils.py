
from personal_ai_assistant.capstone.json_utils import (
    strip_json_code_fence,
)


def test_strip_json_code_fence():
    response = """```json
{
    "intent": "reminder",
    "task": "call John",
    "date": "tomorrow"
}
```"""

    expected = """{
    "intent": "reminder",
    "task": "call John",
    "date": "tomorrow"
}"""

    result = strip_json_code_fence(response)

    assert result == expected


def test_raw_json_is_unchanged():
    response = """{
    "intent": "reminder",
    "task": "call John",
    "date": "tomorrow"
}"""

    result = strip_json_code_fence(response)

    assert result == response
