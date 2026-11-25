from personal_ai_assistant.capstone.intent_prompts import (
    INTENT_CLASSIFICATION_PROMPT
)

prompt = INTENT_CLASSIFICATION_PROMPT.render(
    user_message="Remind me to call John tomorrow"
)

print(prompt)