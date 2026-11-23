from .models import Message
from .protocols import ResponseGenerator
from .exceptions import EmptyMessageError

class Assistant:
    def __init__(
        self,
        name: str,
        assistant_id: str,
        generator: ResponseGenerator,
        message_count: int = 0
    ):
        self.name = name
        self.assistant_id = assistant_id
        self.generator = generator
        self._message_count = message_count
        self.history: list[Message] = []

    @property
    def message_count(self) -> int:
        return self._message_count

    def get_info(self) -> str:
        return (
            f"Name: {self.name} | "
            f"ID: {self.assistant_id} | "
            f"Messages: {self.message_count}"
        )

    def generate_response(self, message: str) -> str:
        if not message.strip():
            raise EmptyMessageError("Message cannot be empty")
        response = self.generator.generate(message)

        self._message_count += 1
        self.history.append(Message(role="user", content=message))
        self.history.append(Message(role="assistant", content=response))

        return response

    
    def restore_history(self, history: list[Message]) -> None:
        self.history = history

        self._message_count = sum(
            1 for message in history
            if message.role == "user"
        )

