history = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "Explain RAG"},
    {"role": "assistant", "content": "RAG combines retrieval and generation."},
    {"role": "user", "content": "Explain agents"},
    {"role": "assistant", "content": "Agents can use tools to complete tasks."}
]

user_message_contents = [
    message["content"]
    for message in history
    if message["role"] == "user"
]

for index, message in enumerate(user_message_contents, start=1):
    print(f"{index}. {message}")

roles = {
    message["role"]
    for message in history
}



message_counts = {
    "user": 0,
    "assistant": 0
}

for message in history:
    role = message["role"]
    message_counts[role] += 1

print("Message counts:")

for role, count in message_counts.items():
    print(f"{role}: {count}")


last_messages = history[-2:]

print("\nLast 2 messages:")

for message in last_messages:
    print(f"{message['role']}: {message['content']}")
