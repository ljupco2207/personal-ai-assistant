api_response = {
    "model": "example-llm",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Python is great!"
            }
        },
        {
            "index": 1,
            "message": {
                "role": "assistant",
                "content": "Swift is great too!"
            }
        },
        {
            "index": 2,
            "message": {
                "role": "assistant",
                "content": "AI Engineering is exciting!"
            }
        }
    ],
    "usage": {
        "input_tokens": 100,
        "output_tokens": 60
    }
}

# Task 1: Print model name
print(f"Model name: {api_response['model']}")

# Task 2: Print second response safely
choices = api_response.get("choices", [])

if len(choices) > 1:
    print(f"Second response: {choices[1]['message']['content']}")

# Task 3: Extract all response contents
responses = [
    choice["message"]["content"]
    for choice in choices
]

# Task 4: Print all responses
if not responses:
    print("No responses available.")
else:
    print("All responses:")

    for index, response in enumerate(responses, start=1):
        print(f"{index}. {response}")

# Task 5: Calculate total tokens
usage = api_response.get("usage", {})

total_tokens = (
    usage.get("input_tokens", 0)
    + usage.get("output_tokens", 0)
)

print(f"Total tokens: {total_tokens}")
