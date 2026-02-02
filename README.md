# Taranis AI summarize-bot Bot

Bot for creating summaries of texts.
Available models:
- t5 (https://huggingface.co/deutsche-telekom/mt5-small-sum-de-en-v1) - DE & EN, *Default*
- bart (https://huggingface.co/facebook/bart-large-cnn) - EN only
- pegasus (https://huggingface.co/google/pegasus-xsum) - EN only


## Pre-requisites

- uv - https://docs.astral.sh/uv/getting-started/installation/
- docker (for building container) - https://docs.docker.com/engine/

Create a python venv and install the necessary packages for the bot to run.

```bash
uv venv
source .venv/bin/activate
uv sync --all-extras --dev
```

## Usage

You can run your bot locally with

```bash
flask run --port 5500
# or
granian app --port 5500
```

You can set configs either via a `.env` file or by setting environment variables directly.
available configs are in the `config.py`
You can select the model via the `MODEL` env var. E.g.:

```bash
MODEL=bart flask run
```

You can specify the minimum and maximum number of tokens that the summary should have with the `MIN_LEN` and `MAX_LEN` env variables respectively.
You can also choose the number of beams for beam search with the `NUM_BEAMS` env variable. 


## Docker

You can also create a Docker image out of this bot. For this, you first need to build the image with the build_container.sh

You can specify which model the image should be built with the MODEL environment variable. If you omit it, the image will be built with the default model.

```bash
MODEL=<model_name> ./build_container.sh
```

then you can run it with:

```bash
docker run -p 5500:8000 <image-name>:<tag>
```

If you encounter errors, make sure that port 5500 is not in use by another application.


## Test the bot

Once the bot is running, you can send test data to it on which it runs its inference method:

```bash
> curl -X POST http://127.0.0.1:5500 -H "Content-Type: application/json" -d '{"text": "New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York. A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband. Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared I do five more times, sometimes only within two weeks of each other. In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her first and only marriage. Barrientos, now 39, is facing two criminal counts of offering a false instrument for filing in the first degree, referring to her false statements on the 2010 marriage license application, according to court documents. Prosecutors said the marriages were part of an immigration scam. On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further. After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002. All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say. Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages. Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted. The case was referred to the Bronx District Attorney Office by Immigration and Customs Enforcement and the Department of Homeland Security Investigation Division. Seven of the men are from so-called red-flagged countries, including Egypt, Turkey, Georgia, Pakistan and Mali. Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force."}'
> {"summary":"Liana Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say. Seven of the men are from so-called red-flagged countries, including Egypt, Turkey, Georgia, Pakistan and Mali. Her eighth husband was deported in 2006 to his native Pakistan."}
```

You can also set up authorization via the `API_KEY` env var. In this case, you need to send the API_KEY as an Authorization header:

```bash
> curl -X POST http://127.0.0.1:5500/  -H "Authorization: Bearer api_key" -H "Content-Type: application/json"   -d '{"text": "Text to summarize ..."}'
```

## Development

If you want to contribute to the development of this bot, make sure you set up your pre-commit hooks correctly:

- Install pre-commit (https://pre-commit.com/)
- Setup hooks: `> pre-commit install`


## License

EUROPEAN UNION PUBLIC LICENCE v. 1.2
