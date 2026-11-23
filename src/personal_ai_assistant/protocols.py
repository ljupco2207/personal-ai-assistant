from typing import Protocol


class ResponseGenerator(Protocol):
    def generate(self, message: str) -> str:
        ...