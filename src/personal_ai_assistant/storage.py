import json
import logging
from pathlib import Path
from dataclasses import asdict
from .models import Message

logger = logging.getLogger(__name__)

def save_history(
    history: list[Message],
    filename: str | Path
) -> None:
    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    history_data = [
        asdict(message)
        for message in history
    ]

    with path.open("w", encoding="utf-8") as file:
        json.dump(history_data, file, indent=2)
    logger.info(
        "Saved %d messages to %s",
        len(history),
        path
    )

def load_history(filename: str | Path) -> list[Message]:
    path = Path(filename)
    print(f"DEBUG: Reading file from {path.resolve()}")
    try: 
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        history = [
            Message(**item)
            for item in data
        ]
        logger.info(
            "Loaded %d messages from %s",
            len(history),
            path
        )
        return history
    except FileNotFoundError:
        logger.warning("History file not found: %s", path)
        return []
    except json.JSONDecodeError:
        logger.error("Invalid JSON in %s", path)
        raise
