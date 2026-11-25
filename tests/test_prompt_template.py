import pytest

from personal_ai_assistant.capstone.prompt_template import (
    PromptTemplate,
    PromptTemplateError
)


def test_prompt_template_renders_variables():
    template = PromptTemplate(
        "Explain {topic} to a {audience}."
    )

    result = template.render(
        topic="RAG",
        audience="Swift developer",
    )

    assert result == "Explain RAG to a Swift developer."


def test_prompt_template_missing_variable():
    template = PromptTemplate(
        "Explain {topic} to a {audience}."
    )

    with pytest.raises(
        PromptTemplateError,
        match="Missing template variables: audience",
    ):
        template.render(topic="RAG")