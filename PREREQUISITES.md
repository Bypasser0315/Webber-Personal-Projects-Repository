<div align="center">

[Overview](README.md) &nbsp;&nbsp;|&nbsp;&nbsp; [**Prerequisites**](PREREQUISITES.md)

</div>

# Prerequisites

Python 3.11 is the version these projects were written with. Notebook projects need Jupyter Notebook, JupyterLab, or the notebook editor in Cursor. Browser projects need Google Chrome installed. Selenium 4 downloads a matching ChromeDriver on its own.

## Gradio App

Folder: `Gradio Apps/Web scraper`

- Google Chrome
- An [OpenRouter](https://openrouter.ai) API key. A key with no credits is enough, because the app calls `openrouter/free`.

```bash
cd "Gradio Apps/Web scraper"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY`. Leave the key box in the app blank to use that file.

## Cookie Cooker

Folder: `cookiecooker`

- Google Chrome
- Selenium

```bash
pip install selenium
```

Open `autocookieclicker.ipynb` and run the cells from top to bottom.

## WhatsApp Bot

Folder: `WhatsApp Bot`

- Google Chrome
- pandas and Selenium
- A WhatsApp account, and WhatsApp Web in English
- After the first cell opens Chrome, scan the QR code in that window with the WhatsApp app on your phone. The notebook does not work until that scan is done. Scan once each time you run the first cell.

```bash
pip install pandas selenium
```

Put one `.csv` and one `.txt` next to `WhatsappAutomaterFinal.ipynb`.

```csv
Name,Phone Number
Ada,85291234567
```

Phone numbers need the country code, with no `+`, spaces, or dashes. In the text file, write `[name]` where the person's name should go, and save it as UTF-8. When the first cell asks for an image, enter a full path with no quotes, or enter `NA` for text only.

The steps for that folder are also in `WhatsApp Bot/PREREQUISITES.md`.

## HKTV Mall scraper

Folder: `HKTV Mall Web Scraping Demonstration`

- Google Chrome
- Selenium, BeautifulSoup, pandas, openpyxl, and matplotlib

```bash
pip install selenium beautifulsoup4 pandas openpyxl matplotlib jupyter
```

Open `hktvscrape.ipynb` and run it from top to bottom. When it asks for a table name, type a filename without `.xlsx`.

## Sorting algorithms

Folder: `Sorting Algorithms`

Python 3 is enough. These programs use only the standard library.

```bash
python bubble_sort.py
```

`bogo_sort.py` and `random_quick_sort.py` run the same way. Type numbers, then type `end`.

## IAL D1 papers

Folder: `IAL D1 Papers`

- The source papers in `Past Papers`
- pypdf and PyMuPDF

```bash
pip install pypdf pymupdf jupyter
```

Open `D1management.ipynb` and run it from top to bottom. The topic PDFs are written to `D1_Sorted_Final`.
