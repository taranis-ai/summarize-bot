from summarize_bot.bart_summarize import BartSummarize
from summarize_bot.pegasus_summarize import PegasusSummarize
from summarize_bot.config import Config


async def test_summarize_bart(article: tuple[str, list], bart_model: BartSummarize):
    content, expected = article
    result = await bart_model.predict(content)
    assert sum(word in result for word in expected) >= 1, f"No expected keywords were found in the summary: {result}"
    assert len(result) < Config.max_new_tokens * 2.5, f"Summary exceeds maximum length.: {len(result)} > {Config.max_new_tokens}"
    assert len(result) > Config.min_length, f"Summary is shorter than minimum length.: {len(result)} < {Config.min_length}"


async def test_summarize_pegasus(article: tuple[str, list], pegasus_model: PegasusSummarize):
    content, expected = article
    result = await pegasus_model.predict(content)
    assert sum(word in result for word in expected) >= 1, f"No expected keywords were found in the summary: {result}"
    assert len(result) < Config.max_new_tokens * 2.5, f"Summary exceeds maximum length.: {len(result)} > {Config.max_new_tokens}"
    assert len(result) > Config.min_length, f"Summary is shorter than minimum length.: {len(result)} < {Config.min_length}"
