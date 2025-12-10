from transformers import pipeline, T5Tokenizer
from summarize_bot.config import Config


class T5:
    model_name = "deutsche-telekom/mt5-small-sum-de-en-v1"

    def __init__(self):
        tokenizer = T5Tokenizer.from_pretrained(self.model_name, legacy=True)
        self.summarizer = pipeline("summarization", model=self.model_name, tokenizer=tokenizer)

    async def predict(self, text: str) -> str:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < Config.MAX_LEN:
            return text

        summary = self.summarizer(
            text,
            max_new_tokens=Config.MAX_LEN,
            num_beams=Config.NUM_BEAMS,
            min_length=Config.MIN_LEN,
            early_stopping=True,
        )

        if isinstance(summary, list) and summary:
            return summary[0]["summary_text"]
        raise ValueError("Summarization failed or returned an unexpected result.")
