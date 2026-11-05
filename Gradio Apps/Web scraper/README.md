# Web Scraper (Gradio)

Scrapes a webpage with Selenium, then uses an OpenRouter model to summarise a website then provide an output. It can also perform other functions besides a summary.

# Example

This is the target website: https://www.bbc.com/future/article/20261029-the-people-who-only-need-four-hours-sleep 

The website has 3 types of outputs to choose from: Word, Markdown, PDF. The PDF can be saved, although images cannot be provided.

Level of Detail can be chosen, from a very simple summary to a detailed report. A free [OpenRouter](https://openrouter.ai/) model is chosen, so do not worry about token usage.

Here is an example:

<img width="1939" height="874" alt="Screenshot 2026-11-03 224452" src="https://github.com/user-attachments/assets/fe0422fc-c423-4358-9fac-38160d013d0f" />

<img width="1288" height="657" alt="Screenshot 2026-11-03 224543" src="https://github.com/user-attachments/assets/f1bf5c8f-cc30-43dc-bf56-4342695a5a1f" />

Try with the other output formats!

## Setup

1. Install [Google Chrome](https://www.google.com/chrome/) (Selenium drives a real browser).
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Rewrite the env variable to be your [OpenRouter](https://openrouter.ai) API Key:
```env
OPENROUTER_API_KEY=your-key-here
```

You can obtain one easily by clicking the link, then click "Get API Key" on the website front page, then press "+New key". Note that you may have to open an account.

## Run

```bash
python app.py
```

Then open the local Gradio URL shown in the terminal.

## Tips

- Leave the API key field blank in the UI to use `OPENROUTER_API_KEY` from `.env`.
- Raise the **Lag** slider if scraping fails on slow pages (15–20 is a good starting point). If your device has poor internet, you may have to set this value higher.
- Older experimental versions live in `archive/`.
