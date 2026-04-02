import httpx

from summarize_bot.config import Config


class Bitnet:
    model_name = "bitnet"

    def __init__(self):
        self.base_url = Config.BITNET_SERVER_URL.rstrip("/")
        self.timeout = Config.BITNET_TIMEOUT_SECONDS
        self.temperature = Config.BITNET_TEMPERATURE

    async def predict(self, text: str) -> dict[str, str]:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < Config.MAX_LEN:
            return {"summary": text}

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You summarize articles. Return only the summary text with no preamble, bullets, or commentary. "
                        f"Keep the summary concise and target roughly {Config.MIN_LEN} to {Config.MAX_LEN} characters."
                    ),
                },
                {"role": "user", "content": text},
            ],
            "temperature": self.temperature,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/v1/chat/completions", json=payload)

        response.raise_for_status()
        summary = self._extract_summary(response.json())
        return {"summary": summary}

    def _extract_summary(self, data: dict) -> str:
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("BitNet response did not contain choices.")

        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            raise ValueError("BitNet response choice had an unexpected format.")

        message = first_choice.get("message")
        if not isinstance(message, dict):
            raise ValueError("BitNet response did not contain a message.")

        content = message.get("content")
        if not isinstance(content, str):
            raise ValueError("BitNet response message did not contain text content.")

        summary = content.strip()
        if not summary:
            raise ValueError("BitNet response returned an empty summary.")

        return summary
