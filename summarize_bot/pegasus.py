from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from summarize_bot.config import Config


class Pegasus:
    model_name = "google/pegasus-xsum"

    def __init__(self):
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.summarizer = PegasusForConditionalGeneration.from_pretrained(self.model_name)

    async def predict(self, text: str) -> str:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < Config.MAX_LEN:
            return text

        inputs = self.tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
        summary_ids = self.summarizer.generate(
            inputs.input_ids,
            max_new_tokens=Config.MAX_LEN,
            min_length=Config.MIN_LEN,
            num_beams=Config.NUM_BEAMS,
            early_stopping=True,
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
