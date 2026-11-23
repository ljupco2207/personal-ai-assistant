import json
from .assistant import Assistant
from .generators import EchoGenerator
from .storage import save_history, load_history
from pathlib import Path
from .logging_config import configure_logging
from .exceptions import EmptyMessageError

def main() -> None:
    configure_logging()
    
    assistant = Assistant(
        name="Echo AI",
        assistant_id="001",
        generator=EchoGenerator()
    )

    history_file = Path("data") / "conversation.json"


    print(assistant.get_info())
    print(f"Welcome to {assistant.name}!")

    while True:
        user_message = input("You: ")
        normalized_message = user_message.strip()
        command = normalized_message.lower()

        if command == "exit":
            print("Goodbye!")
            print(f"Total messages: {assistant.message_count}")
            break

        if command == "/help":
            show_help()
            continue
        elif command == "/stats":
            print(f"Total valid messages: {assistant.message_count}")

            user_messages = [
                message
                for message in assistant.history
                if message.role == "user"
            ]

            assistant_messages = [
                message
                for message in assistant.history
                if message.role == "assistant"
            ]
            roles = {
                message.role
                for message in assistant.history
            }
          
            print(f"User history entries: {len(user_messages)}")
            print(f"Assistant history entries: {len(assistant_messages)}")
            print(f"Unique roles: {len(roles)}")

            continue
        elif command == "/history":
            for index, message in enumerate(assistant.history, start=1):
                print(f"{index}. {message.role}: {message.content}")
            continue
        elif command == "/recent":
            recent_messages = assistant.history[-4:]
            for index, message in enumerate(recent_messages, start=1):
                print(f"{index}. {message.role}: {message.content}")
            continue

        elif command == "/users":
            user_messages = [
                message.content
                for message in assistant.history
                if message.role == "user"
            ]

            if not user_messages:
                print("No user messages yet.")
            else:
                for index, message in enumerate(user_messages, start=1):
                    print(f"{index}. {message}")

            continue
        elif command == "/save":
            try:
                save_history(assistant.history, history_file)
                print("Conversation saved successfully.")
            except OSError as error:
                print(f"Could not save conversation: {error}")
            continue
        elif command == "/load":
            try:
                history = load_history(history_file)
                assistant.restore_history(history)
                print(f"Loaded {len(history)} messages.")
            except json.JSONDecodeError:
                print("Could not load history: invalid JSON.")
            except OSError as error:
                print(f"Could not read history: {error}")
            continue

        if not normalized_message:
            print("Please enter a message.")
            continue

        try:
            response = assistant.generate_response(normalized_message)
            print(f"Assistant: {response}")
        except EmptyMessageError as error:
             print(f"Invalid message: {error}")


def show_help() -> None:
    print("Available commands:")
    print("/help - Show available commands")
    print("/stats - Show message statistics")
    print("/history - Show conversation history")
    print("/recent - Show recent history")
    print("/users - Show only user messages")
    print("/save - Save conversation history")
    print("/load - Restore saved conversation history")
    print("exit - Close the assistant")


if __name__ == "__main__":
    main()