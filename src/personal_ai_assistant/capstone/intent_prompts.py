from personal_ai_assistant.capstone.prompt_template import (
    PromptTemplate,
)

INTENT_CLASSIFICATION_PROMPT = PromptTemplate(
    template=(
        "You are an intent classifier.\n"
        "Classify the user's message into exactly one category:\n"
        "calendar, reminder, general.\n\n"
        "Examples:\n"
        "User: Schedule a meeting tomorrow.\n"
        "Category: calendar\n\n"
        "User: Remind me to buy milk.\n"
        "Category: reminder\n\n"
        "User: Explain Python decorators.\n"
        "Category: general\n\n"
        "Return only the category name.\n\n"
        "User: {user_message}\n"
        "Category:"
    )
)