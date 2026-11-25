from personal_ai_assistant.capstone.intent_prompts import (
    INTENT_CLASSIFICATION_PROMPT,
)


def test_intent_prompt_contains_examples():
    prompt = INTENT_CLASSIFICATION_PROMPT.render(
        user_message="Remind me to call John."
    )

    assert "Category: calendar" in prompt
    assert "Category: reminder" in prompt
    assert "Category: general" in prompt

    assert "User: Remind me to call John." in prompt
    assert prompt.endswith("Category:")