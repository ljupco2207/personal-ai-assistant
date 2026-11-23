import asyncio
import json

from pathlib import Path
from .models import Message, Role
from .exceptions import StorageError


class JSONConversationStorage:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    
    async def save(self, messages: list[Message]) -> None:
        data = [
            {
                "role": message.role.value,
                "content": message.content
            }
            for message in messages
        ]

        try:
            await asyncio.to_thread(
                self._write_json,
                data
            )
        except OSError as error:
            raise StorageError(
                "Failed to save conversation history"
            ) from error


    def _write_json(self, data: list[dict]) -> None:
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.file_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=2)

 

    async def load(self) -> list[Message]:
        if not self.file_path.exists():
            return []

        try:
            data = await asyncio.to_thread(
                self._read_json
            )

            return [
                Message(
                    role=Role(item["role"]),
                    content=item["content"]
                )
                for item in data
            ]

        except (
            OSError,
            ValueError,
            KeyError,
            TypeError
        ) as error:
            raise StorageError(
                "Failed to load conversation history"
            ) from error

    def _read_json(self) -> list[dict]:
        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)
