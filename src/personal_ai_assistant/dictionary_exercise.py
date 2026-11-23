api_response = {
    "id": "response_001",
    "model": "example-llm",
    "usage": {
        "input_tokens": 150,
        "output_tokens": 75
    },
    "message": {
        "role": "assistant",
        "content": "Python is great for AI Engineering!"
    }
}

print(f"Model name: {api_response['model']}")

print(f"Assistant content: {api_response['message']['content']}")

total = (
    api_response["usage"]["input_tokens"]
    + api_response["usage"]["output_tokens"]
)

print(f"Total tokens: {total}")

print(f"Finish reason: {api_response.get('finish_reason', 'unknown')}")

