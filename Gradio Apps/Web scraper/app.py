# Gradio web scraper — scrape a page, then summarise it with OpenRouter.
try:
    import base64
    import html
    import os
    import re
    import tempfile
    import time
    from datetime import datetime
    from pathlib import Path

    import gradio as gr
    import markdown
    import requests
    from bs4 import BeautifulSoup as bs
    from dotenv import load_dotenv
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    print("All packages imported successfully")
except ImportError as e:
    print(f"Error importing packages: {e}")
    raise SystemExit(1) from e

load_dotenv(Path(__file__).resolve().parent / ".env")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
_PLACEHOLDER_KEYS = {
    "",
    "TESTESTEST",
    "paste-your-openrouter-key-here",
    "your-key-here",
}


def web_scrape(url, time_rate):
    chrome_options = Options()
    # Uncomment to run without opening a visible browser window:
    # chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(time_rate * 0.5)

        # Click common cookie / consent buttons when present
        cookie_keywords = ["Accept", "Agree", "Allow all", "Dismiss", "Accept Cookies"]
        for keyword in cookie_keywords:
            try:
                cookie_button = driver.find_element(
                    By.XPATH,
                    f"//button[contains(text(), '{keyword}')] | //button[contains(., '{keyword}')]",
                )
                cookie_button.click()
                print(f"Automatically clicked cookie button: '{keyword}'")
                time.sleep(2)
                break
            except Exception:
                continue

        # Scroll to trigger lazy-loaded content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(time_rate * 0.1)

        soup = bs(driver.page_source, "html.parser")
        body_content = soup.body
        if not body_content:
            return "Could not find body tag."

        for script_or_style in body_content(["script", "style"]):
            script_or_style.extract()

        cleaned_content = body_content.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        return cleaned_content.replace("\xa0", " ")
    finally:
        driver.quit()


def ai_prompt(prompt, api_key, system_prompt, time_rate):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }

    time.sleep(time_rate * 0.8)
    response = None
    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        output = response.json()["choices"][0]["message"]["content"]
        time.sleep(time_rate * 0.4)
        return output
    except Exception as e:
        print("\n--- API CALL FAILED ---")
        print(f"Error details: {e}")
        if response is not None and response.status_code != 200:
            print(f"Server response text: {response.text}")
        print("-----------------------\n")
        raise


def get_api_key():
    api_key = (OPENROUTER_API_KEY or "").strip()
    if api_key in _PLACEHOLDER_KEYS:
        raise ValueError(
            "No API key found. Put OPENROUTER_API_KEY in your .env file in this folder."
        )
    return api_key


def unwrap_markdown_fence(text):
    stripped = (text or "").strip()
    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return stripped


def pdf_output_path(title):
    cleaned = re.sub(r'[<>:"/\\|?*\n\r\t]', "", title or "").strip().rstrip(".")
    if not cleaned:
        cleaned = "My Report"
    return Path.cwd() / f"{cleaned}.pdf"


def markdown_to_pdf(markdown_text, title):
    """Render Markdown to HTML, then print that page to a PDF."""
    body = markdown.markdown(
        unwrap_markdown_fence(markdown_text),
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )
    safe_title = html.escape(title or "My Report")
    document = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{safe_title}</title>
<style>
  @page {{ size: A4; margin: 16mm; }}
  body {{
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.45;
    color: #1a1a1a;
  }}
  h1 {{ font-size: 22pt; margin: 0 0 0.6em; }}
  h2 {{ font-size: 16pt; margin: 1.1em 0 0.4em; }}
  h3 {{ font-size: 13pt; margin: 1em 0 0.3em; }}
  p {{ margin: 0.4em 0; }}
  ul, ol {{ margin: 0.4em 0 0.4em 1.2em; }}
  table {{ border-collapse: collapse; width: 100%; margin: 0.8em 0; }}
  th, td {{ border: 1px solid #cccccc; padding: 6px 8px; text-align: left; vertical-align: top; }}
  th {{ background: #f3f3f3; }}
  code {{ font-family: Consolas, monospace; background: #f5f5f5; padding: 1px 4px; }}
  pre {{ background: #f5f5f5; padding: 10px; white-space: pre-wrap; }}
  pre code {{ background: transparent; padding: 0; }}
  blockquote {{ border-left: 3px solid #cccccc; margin: 0.6em 0; padding-left: 12px; color: #444444; }}
  img {{ max-width: 100%; }}
</style>
</head>
<body>
<h1>{safe_title}</h1>
{body}
</body>
</html>"""

    output_path = pdf_output_path(title)
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = Path(temp_dir) / "report.html"
        html_path.write_text(document, encoding="utf-8")

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(html_path.resolve().as_uri())
            pdf = driver.execute_cdp_cmd(
                "Page.printToPDF",
                {
                    "printBackground": True,
                    "preferCSSPageSize": True,
                    "paperWidth": 8.27,
                    "paperHeight": 11.69,
                },
            )
        finally:
            driver.quit()

    output_path.write_bytes(base64.b64decode(pdf["data"]))
    return output_path


def timeline_instruction(timeline):
    if not timeline:
        return ""
    return (
        "Structure the answer as a timeline: use a level-2 heading named Timeline, "
        "then list events in chronological order. "
        "Each event should be a level-3 heading with the date or time period, "
        "followed by one or two sentences. "
        "If exact dates are missing, use the best approximate order you can infer from the page."
    )


def build_prompt(output_format, goal, detail_instruction, cleaned_content, table, specs, timeline):
    markdown_like = output_format in ("Markdown", "PDF")
    timeline_note = timeline_instruction(timeline)
    extra_bits = []
    if timeline_note:
        extra_bits.append(timeline_note)
    if specs:
        extra_bits.append(f"Additional Customizations: {specs}")
    extras = "\n".join(extra_bits)

    if markdown_like and table and specs:
        return (
            f"User Goal: {goal}. {detail_instruction}\n\n"
            f"Based on this scraped text:\n{cleaned_content}\n\n"
            "Format style: Markdown. You MUST include a Markdown table. "
            "Ensure every single row of the table starts on a brand new line using proper formatting.\n"
            f"{extras}"
        )
    if markdown_like and table:
        return (
            f"User Goal: {goal}. {detail_instruction}\n\n"
            f"Based on this scraped text:\n{cleaned_content}\n\n"
            "Format style: Markdown. You MUST include a Markdown table. "
            "Ensure every single row of the table starts on a brand new line using proper formatting.\n"
            f"{timeline_note}"
        )
    if markdown_like and (specs or timeline):
        return (
            f"User Goal: {goal}. {detail_instruction} "
            f"Based on this scraped text:{cleaned_content}. Format style: Markdown.\n"
            f"{extras}"
        )
    if markdown_like:
        return (
            f"User Goal: {goal}. {detail_instruction}\n\n"
            f"Based on this scraped text:\n{cleaned_content}\n\n"
            "Format style: Markdown. Use headings, lists, and tables where they make the content clearer.\n"
            f"{timeline_note}"
        )
    return (
        f"User Goal: {goal}. {detail_instruction} "
        f"Based on this scraped text:{cleaned_content}. Format style: {output_format}."
    )


def format_history_display(history):
    if not history:
        return "*No recorded outputs yet. Runs that produce Markdown or PDF are saved here.*"
    blocks = []
    for index, item in enumerate(reversed(history), start=1):
        blocks.append(f"### {index}. {item['title']}")
        blocks.append(f"*Recorded {item['when']} · {item['url']}*")
        blocks.append(item["markdown"])
        blocks.append("---")
    return "\n\n".join(blocks)


def history_markdown_blob(history):
    if not history:
        return ""
    parts = [f"# Past outputs ({len(history)} runs)\n"]
    for index, item in enumerate(history, start=1):
        parts.append(f"## {index}. {item['title']}")
        parts.append(f"*Recorded {item['when']} · {item['url']}*")
        parts.append(f"**Goal:** {item['goal']}")
        parts.append(item["markdown"])
        parts.append("\n---\n")
    return "\n".join(parts)


def append_history(history, url, goal, title, markdown_text):
    history = list(history or [])
    history.append(
        {
            "title": (title or "My Report").strip() or "My Report",
            "url": (url or "").strip(),
            "goal": (goal or "").strip(),
            "when": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "markdown": unwrap_markdown_fence(markdown_text),
        }
    )
    return history


def export_history_pdf(history):
    if not history:
        raise gr.Error("There are no recorded outputs yet.")
    blob = history_markdown_blob(history)
    pdf_path = markdown_to_pdf(blob, "Past outputs")
    return str(pdf_path)


def clear_run_outputs():
    return (
        gr.update(value="", visible=True),
        gr.update(value="", visible=False),
        gr.update(value=None, visible=False),
    )


def status_update(message):
    return gr.update(value=message, visible=True)


def run_scraper(
    url,
    goal,
    detail_level,
    time_delay,
    output_format,
    title,
    table,
    specs,
    timeline,
    history,
):
    history = list(history or [])
    cleared_text, cleared_md, cleared_file = clear_run_outputs()

    if output_format == "PDF":
        yield (
            status_update(
                f"Starting program with PDF generation, estimated time is {time_delay * 8 + 5} seconds"
            ),
            cleared_md,
            cleared_file,
            history,
            format_history_display(history),
        )
    else:
        yield (
            status_update(
                f"Starting program with output as {output_format}, estimated time is {time_delay * 8} seconds"
            ),
            cleared_md,
            cleared_file,
            history,
            format_history_display(history),
        )

    time.sleep(time_delay * 0.1)
    yield status_update("Scraping website..."), cleared_md, cleared_file, history, format_history_display(history)
    cleaned_content = web_scrape(url, time_delay)
    time.sleep(time_delay * 0.5)

    try:
        api_key = get_api_key()
        yield status_update("API key ready"), cleared_md, cleared_file, history, format_history_display(history)
    except Exception as e:
        yield status_update(f"Setup failed: {e}"), cleared_md, cleared_file, history, format_history_display(history)
        return

    yield status_update("Building prompt..."), cleared_md, cleared_file, history, format_history_display(history)
    system_prompt = (
        "You are a precise web-scraping content extraction assistant. "
        f"Your job is to extract content based on the user's goal: {goal}, "
        "ignoring all website navigation, advertisements, and popups."
    )
    detail_instruction = f"The final response must be {detail_level}."
    big_prompt = build_prompt(
        output_format, goal, detail_instruction, cleaned_content, table, specs, timeline
    )

    time.sleep(time_delay * 0.5)
    yield status_update("Asking the model..."), cleared_md, cleared_file, history, format_history_display(history)
    output = ai_prompt(
        prompt=big_prompt,
        api_key=api_key,
        system_prompt=system_prompt,
        time_rate=time_delay,
    )

    if output_format == "PDF":
        yield status_update("Rendering Markdown into a PDF..."), cleared_md, cleared_file, history, format_history_display(history)
        pdf_path = markdown_to_pdf(output, title)
        history = append_history(history, url, goal, title, output)
        yield (
            status_update("Your PDF has been generated successfully!"),
            gr.update(visible=False, value=""),
            gr.update(visible=True, value=str(pdf_path)),
            history,
            format_history_display(history),
        )
        return

    if output_format == "Markdown":
        history = append_history(history, url, goal, title or "My Report", output)
        yield (
            status_update("Markdown output is ready below."),
            gr.update(visible=True, value=output),
            gr.update(visible=False, value=None),
            history,
            format_history_display(history),
        )
        return

    yield (
        gr.update(visible=True, value=output),
        gr.update(visible=False, value=""),
        gr.update(visible=False, value=None),
        history,
        format_history_display(history),
    )


def toggle_format_options(status):
    if status == "PDF":
        return (
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(value=False, visible=True),
            gr.update(value=False, visible=True),
            gr.update(value="", visible=True),
        )
    if status == "Markdown":
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(value=False, visible=True),
            gr.update(value=False, visible=True),
            gr.update(value="", visible=True),
        )
    return (
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(value=False, visible=False),
        gr.update(value=False, visible=False),
        gr.update(value="", visible=False),
    )


with gr.Blocks(title="Web Scraper") as demo:
    output_history = gr.State([])
    gr.Markdown("# Web Scraper\nScrape a page, then turn it into plain text, Markdown, or a PDF rendered from Markdown.")

    with gr.Tabs():
        with gr.Tab("Scraper"):
            with gr.Row():
                with gr.Column(scale=1, min_width=320):
                    url = gr.Textbox(label="Website URL")
                    goal = gr.Textbox(label="What do you need from this website?")
                    detail_level = gr.Dropdown(
                        label="How detailed should the output be?",
                        choices=[
                            "Very Simple",
                            "Simple",
                            "Moderately Detailed",
                            "Detailed",
                            "Very Detailed",
                        ],
                        value="Moderately Detailed",
                    )
                    lag = gr.Slider(
                        2,
                        50,
                        value=15,
                        step=0.1,
                        label="Lag (raise this if your connection is slow; 15–20 is a safe default)",
                    )
                    with gr.Group():
                        gr.Markdown("### Output settings")
                        output_format = gr.Radio(
                            label="Output format",
                            choices=["Plain text", "Markdown", "PDF"],
                            value="Plain text",
                        )
                        title = gr.Textbox(
                            label="Title for your PDF",
                            value="My Report",
                            visible=False,
                        )
                        with gr.Column(visible=False) as md_extras:
                            with gr.Row():
                                md_table = gr.Checkbox(
                                    label="Include a table",
                                    value=False,
                                )
                                md_timeline = gr.Checkbox(
                                    label="Format as a timeline",
                                    value=False,
                                )
                            md_specs = gr.Textbox(
                                label="Extra Markdown customisations",
                                value="",
                            )
                    start_button = gr.Button("Start", variant="primary")

                with gr.Column(scale=2, min_width=320):
                    with gr.Group():
                        gr.Markdown("### Results")
                        text_output = gr.Textbox(label="Status / Text Output", visible=True, lines=6)
                        markdown_output = gr.Markdown(label="Markdown Output", visible=False)
                        file_output = gr.File(label="Download your file (.pdf)", visible=False)

        with gr.Tab("Past outputs"):
            past_outputs_view = gr.Markdown(
                value="*No recorded outputs yet. Runs that produce Markdown or PDF are saved here.*"
            )
            export_past_button = gr.Button("Export all recorded outputs to one PDF", variant="secondary")
            past_pdf_file = gr.File(label="Combined PDF download", visible=True)

    output_format.change(
        fn=toggle_format_options,
        inputs=output_format,
        outputs=[title, md_extras, md_table, md_timeline, md_specs],
    )
    output_format.change(
        fn=clear_run_outputs,
        inputs=None,
        outputs=[text_output, markdown_output, file_output],
    )
    start_button.click(
        fn=run_scraper,
        inputs=[
            url,
            goal,
            detail_level,
            lag,
            output_format,
            title,
            md_table,
            md_specs,
            md_timeline,
            output_history,
        ],
        outputs=[text_output, markdown_output, file_output, output_history, past_outputs_view],
        api_name="webscraper",
    )
    export_past_button.click(
        fn=export_history_pdf,
        inputs=output_history,
        outputs=past_pdf_file,
    )

if __name__ == "__main__":
    demo.launch()
