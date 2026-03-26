from transformers import pipeline
from summarize_bot.config import Config


class Bart:
    model_name = "facebook/bart-large-cnn"

    def __init__(self):
        self.summarizer = pipeline("summarization", model=self.model_name)

    async def predict(self, text: str) -> dict[str, str]:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < Config.MAX_LEN:
            return {"summary": text}

        summary = self.summarizer(
            text,
            max_new_tokens=Config.MAX_LEN,
            num_beams=Config.NUM_BEAMS,
            min_length=Config.MIN_LEN,
            early_stopping=True,
        )

        if isinstance(summary, list) and summary:
            return {"summary": summary[0]["summary_text"]}
        raise ValueError("Summarization failed or returned an unexpected result.")
