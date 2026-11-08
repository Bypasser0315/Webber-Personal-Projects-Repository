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

3. Open `.env.example`, paste your [OpenRouter](https://openrouter.ai) API key in place of the placeholder, then rename the file to `.env` in this folder.

You can obtain a key from OpenRouter: open the site, click **Get API Key**, then **+ New key**. You may need to create an account first.

## Run

```bash
python app.py
```

Then open the local Gradio URL shown in the terminal.

## Tips

- The app reads `OPENROUTER_API_KEY` from `.env` only. Do not commit `.env`.
- Markdown and PDF runs can use **Include a table** and **Format as a timeline**. Finished Markdown is listed on the **Past outputs** tab; export them to one PDF from there.
- Raise the **Lag** slider if scraping fails on slow pages (15–20 is a good starting point). If your device has poor internet, you may have to set this value higher.
- Older experimental versions live in `archive/`.
