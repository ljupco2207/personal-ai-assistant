import pytest

from personal_ai_assistant.config import load_config

@pytest.fixture(autouse=True)
def disable_dotenv(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")


def test_load_config_success(monkeypatch):
    # Arrange
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("API_TIMEOUT", "15")
    monkeypatch.setenv("APP_ENV", "testing")

    # Act
    config = load_config()

    # Assert
    assert config.api_key == "test-key"
    assert config.timeout == 15.0
    assert config.environment == "testing"


def test_load_config_defaults(monkeypatch):
    # Arrange
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("API_TIMEOUT", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)

    # Act
    config = load_config()

    # Assert
    assert config.timeout == 10.0
    assert config.environment == "development"


def test_load_config_missing_api_key(monkeypatch):
    # Arrange
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("API_TIMEOUT", "15")
    monkeypatch.setenv("APP_ENV", "testing")

    # Act & Assert
    with pytest.raises(
        ValueError,
        match="OPENAI_API_KEY is missing"
    ):
        load_config()

