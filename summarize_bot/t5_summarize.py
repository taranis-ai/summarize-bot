from transformers import pipeline, T5Tokenizer
from summarize_bot.predictor import Predictor
from summarize_bot.config import Config


class T5Summarize(Predictor):
    model_name = "deutsche-telekom/mt5-small-sum-de-en-v1"

    def __init__(self):
        tokenizer = T5Tokenizer.from_pretrained(self.model_name, legacy=True)
        self.summarizer = pipeline("summarization", model=self.model_name, tokenizer=tokenizer)

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
