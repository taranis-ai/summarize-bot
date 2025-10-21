from transformers import pipeline
from summarize_bot.predictor import Predictor
from summarize_bot.config import Config


class BartSummarize(Predictor):
    model_name = "facebook/bart-large-cnn"

    def __init__(self):
        self.summarizer = pipeline("summarization", model=self.model_name)

    async def predict(self, text: str) -> str:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < Config.max_new_tokens:
            return text

        summary = self.summarizer(
            text,
            max_new_tokens=Config.max_new_tokens,
            num_beams=Config.num_beams,
            min_length=Config.min_length,
            early_stopping=True,
        )

        if isinstance(summary, list) and summary:
            return summary[0]["summary_text"]
        raise ValueError("Summarization failed or returned an unexpected result.")
