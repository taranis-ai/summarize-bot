from typing import Literal
from taranis_base_bot.config import CommonSettings


class Settings(CommonSettings):
    MODEL: Literal["t5", "bart", "pegasus", "bitnet"] = "t5"
    PACKAGE_NAME: str = "summarize_bot"
    HF_MODEL_INFO: bool = True
    PAYLOAD_SCHEMA: dict[str, dict] = {"text": {"type": "str", "required": True}}
    MAX_LEN: int = 280
    MIN_LEN: int = 80
    NUM_BEAMS: int = 4
    BITNET_SERVER_URL: str = "http://bitnet-server:8080"
    BITNET_TIMEOUT_SECONDS: float = 30.0
    BITNET_TEMPERATURE: float = 0.1

Config = Settings()
