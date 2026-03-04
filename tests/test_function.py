from summarize_bot.bart import Bart
from summarize_bot.pegasus import Pegasus
from summarize_bot.t5 import T5
from summarize_bot.config import Config


async def test_summarize_bart(article: tuple[str, list], bart_model: Bart):
    content, expected = article
    result = await bart_model.predict(content)
    assert sum(word in result for word in expected) >= 1, f"No expected keywords were found in the summary: {result}"
    assert len(result) < Config.MAX_LEN * 2.5, f"Summary exceeds maximum length.: {len(result)} > {Config.MAX_LEN}"
    assert len(result) > Config.MIN_LEN, f"Summary is shorter than minimum length.: {len(result)} < {Config.MIN_LEN}"


async def test_summarize_pegasus(article: tuple[str, list], pegasus_model: Pegasus):
    content, expected = article
    result = await pegasus_model.predict(content)
    assert sum(word in result for word in expected) >= 1, f"No expected keywords were found in the summary: {result}"
    assert len(result) < Config.MAX_LEN * 2.5, f"Summary exceeds maximum length.: {len(result)} > {Config.MAX_LEN}"
    assert len(result) > Config.MIN_LEN, f"Summary is shorter than minimum length.: {len(result)} < {Config.MIN_LEN}"

async def test_summarize_t5(article: tuple[str, list], t5_model: T5):
    content, expected = article
    result = await t5_model.predict(content)
    assert sum(word in result for word in expected) >= 1, f"No expected keywords were found in the summary: {result}"
    assert len(result) < Config.MAX_LEN * 2.5, f"Summary exceeds maximum length.: {len(result)} > {Config.MAX_LEN}"
    assert len(result) > Config.MIN_LEN, f"Summary is shorter than minimum length.: {len(result)} < {Config.MIN_LEN}"
