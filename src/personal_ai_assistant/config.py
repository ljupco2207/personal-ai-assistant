import os
import math

from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class AppConfig:
    api_key: str
    timeout: float
    environment: str


def load_config() -> AppConfig:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing")

    timeout = float(os.getenv("API_TIMEOUT", "10"))

    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("API_TIMEOUT must be a positive finite number")

    return AppConfig(
        api_key=api_key,
        timeout=timeout,
        environment=os.getenv("APP_ENV", "development")
    )

def main() -> None:
    config = load_config()

    print(f"Environment: {config.environment}")
    print(f"Timeout: {config.timeout}")
    print(f"API key configured: {bool(config.api_key)}")


if __name__ == "__main__":
    main()
