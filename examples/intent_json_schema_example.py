import json

from personal_ai_assistant.capstone.structured_models import (
    IntentResult,
)


def main():
    schema = IntentResult.model_json_schema()

    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()