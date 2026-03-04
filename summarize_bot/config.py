from typing import Literal
from taranis_base_bot.config import CommonSettings


class Settings(CommonSettings):
    MODEL: Literal["t5", "bart", "pegasus"] = "t5"
    PACKAGE_NAME: str = "summarize_bot"
    HF_MODEL_INFO: bool = True
    PAYLOAD_SCHEMA: dict[str, dict] = {"text": {"type": "str", "required": True}}
    MAX_LEN: int = 280
    MIN_LEN: int = 80
    NUM_BEAMS: int = 4

Config = Settings()
