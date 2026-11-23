class EchoGenerator:
    def generate(self, message: str) -> str:
        return f"You said: {message}"


class UppercaseGenerator:
    def generate(self, message: str) -> str:
        return message.upper()