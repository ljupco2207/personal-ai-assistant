import anthropic
from anthropic import AsyncAnthropic
from collections.abc import AsyncIterator
from pydantic import ValidationError

from .models import Message, Role, AssistantResponse
from .exceptions import (
    ProviderError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
    ProviderConnectionError,
    ProviderServerError,
)
from .protocols import T


class AnthropicProvider:
    def __init__(self, client: AsyncAnthropic, model: str = "claude-haiku-4-5"):
        self.client = client
        self.model = model

    @staticmethod
    def _prepare_request(messages: list[Message]) -> dict:
        system_messages = [m.content for m in messages if m.role == Role.SYSTEM]
        conversation = [
            {"role": m.role.value, "content": m.content}
            for m in messages if m.role != Role.SYSTEM
        ]
        request = {"messages": conversation}
        if system_messages:
            request["system"] = "\n\n".join(system_messages)
        return request

    async def _create(self, request: dict):
        try:
            return await self.client.messages.create(**request)
        except anthropic.AuthenticationError as error:
            raise ProviderAuthenticationError("Invalid Anthropic API credentials") from error
        except anthropic.RateLimitError as error:
            raise ProviderRateLimitError("Anthropic API rate limit exceeded") from error
        except anthropic.APITimeoutError as error:
            raise ProviderConnectionError("Anthropic API request timed out") from error
        except anthropic.APIConnectionError as error:
            raise ProviderConnectionError("Unable to connect to Anthropic") from error
        except anthropic.InternalServerError as error:
            raise ProviderServerError("Anthropic server is temporarily unavailable") from error
        except anthropic.APIStatusError as error:
            raise ProviderError(f"Anthropic API returned HTTP {error.status_code}") from error

    async def generate(self, messages: list[Message]) -> AssistantResponse:
        request = {
            "model": self.model,
            "max_tokens": 1024,
            **self._prepare_request(messages),
        }
        response = await self._create(request)
        content = "\n".join(
            block.text for block in response.content if block.type == "text"
        )
        return AssistantResponse(
            message=Message(role=Role.ASSISTANT, content=content),
            model_name=response.model,
        )

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        request = {
            "model": self.model,
            "max_tokens": 1024,
            **self._prepare_request(messages),
        }
        try:
            async with self.client.messages.stream(**request) as stream:
                async for text in stream.text_stream:
                    yield text
        except anthropic.AuthenticationError as error:
            raise ProviderAuthenticationError("Invalid Anthropic API credentials") from error
        except anthropic.RateLimitError as error:
            raise ProviderRateLimitError("Anthropic API rate limit exceeded") from error
        except anthropic.APITimeoutError as error:
            raise ProviderConnectionError("Anthropic API request timed out") from error
        except anthropic.APIConnectionError as error:
            raise ProviderConnectionError("Unable to connect to Anthropic") from error
        except anthropic.InternalServerError as error:
            raise ProviderServerError("Anthropic server is temporarily unavailable") from error
        except anthropic.APIStatusError as error:
            raise ProviderError(f"Anthropic API returned HTTP {error.status_code}") from error

    async def generate_structured(
        self, messages: list[Message], response_model: type[T]
    ) -> T:
        request = {
            "model": self.model,
            "max_tokens": 1024,
            **self._prepare_request(messages),
            "output_config": {
                "format": {
                    "type": "json_schema",
                    "schema": response_model.model_json_schema(),
                }
            },
        }
        response = await self._create(request)
        if getattr(response, "stop_reason", None) in ("max_tokens", "refusal"):
            raise ProviderError("Claude did not complete the structured response")
        try:
            blocks = response.content
            raw_json = next(block.text for block in blocks if hasattr(block, "text"))
            return response_model.model_validate_json(raw_json)
        except (ValidationError, StopIteration, AttributeError, TypeError, ValueError) as error:
            raise ProviderError("Claude returned an invalid structured response") from error
