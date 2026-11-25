from typing import Literal

from pydantic import BaseModel, ConfigDict, StrictStr


class IntentResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: Literal["calendar", "reminder", "general"]
    task: StrictStr
    date: StrictStr | None