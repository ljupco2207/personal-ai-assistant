from personal_ai_assistant.capstone.prompt_template import (
    PromptTemplate,
)

template = PromptTemplate(
    template=(
        "You are an AI engineering tutor.\n"
        "Explain {topic} to a {audience}.\n"
        "Difficulty level: {level}.\n"
        "Include a practical Python example."
    )
)

prompt = template.render(
    topic="Vector databases",
    audience="Swift developer",
    level="beginner",
)

print(prompt)