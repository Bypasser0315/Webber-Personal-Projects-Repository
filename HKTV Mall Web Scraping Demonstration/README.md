# HKTV Mall Web Scraping Demonstration

This notebook scrapes beef steak search results from [HKTV Mall](https://www.hktvmall.com/) and saves them as a spreadsheet.

It opens the English search page for “beef steak”, walks each result page in Chrome, and records:

- Product name
- Price (HKD)
- The sales figure printed on the card
- A rough origin label: Australian, American, Japanese, New Zealand, or Other
- A product type: Steak, Bar, Dog Food, Jerky, Stick, or Sauce
- Whether the name mentions Wagyu

I built this to practise Selenium and BeautifulSoup, and to compare steak listings by origin. Origin and type are guessed from keywords in the product name, so they are approximate.

The copy of the notebook in this folder already has output from one run: 9 pages, 537 listings.

## What you need

- Python 3
- Google Chrome
- A way to run a Jupyter notebook (Jupyter Notebook, JupyterLab, or the notebook editor in Cursor / VS Code)

```bash
pip install selenium beautifulsoup4 pandas openpyxl jupyter
```

Selenium 4 downloads a matching ChromeDriver for you. A separate driver install is only needed if that automatic step fails.

## How to run

1. Open `hktvscrape.ipynb`.
2. Run the cells from top to bottom.
3. Leave the Chrome window alone while the pages turn. Each page waits until product names appear, then clicks **Next**.
4. When the notebook asks `Table name`, type a filename without `.xlsx`. It saves `{name}.xlsx` in the working directory.

To scrape a different search, change `url` in the setup cell before you run the loop.

## What’s in this folder

| File | Purpose |
| --- | --- |
| `hktvscrape.ipynb` | Scrape, clean, label, save, and a short comparison by origin |
| `README.md` | This file |

## How it works

1. Chrome opens `https://www.hktvmall.com/hktv/en/search_a?keyword=beef%20steak`.
2. A span such as `/  9 Pages` sets how many times the loop runs.
3. Each page is parsed with BeautifulSoup:
   - `div.brand-product-name` — name
   - `div.price` — price text
   - `div.salesNumber-container` — sales text
4. Selenium clicks the button `#sortMenu_next` to move to the next page.
5. Cleaning:
   - Price keeps the number after the first space (the currency token is dropped).
   - Sales text such as `100+` keeps the part before `+`. A blank badge becomes `0`. Commas and spaces are removed.
   - Both columns are converted to numbers. Values that still are not numbers become missing.
6. **Add Classes** labels each row:
   - Origin from `Australia` / `AUS`, `USA` / `United States` / `America`, `NZ` / `New Zealand`, `Japan` / `JP`. Anything else stays `Other`.
   - Type from `Bar`, `Dog`, `Jerky`, `Stick`, or `Sauce`. Anything else stays `Steak`. If a name matches more than one of these, the later rule wins.
   - `Wagyu?` is `True` when the name contains `Wagyu`.
7. The comparison cells keep rows whose type is `Steak`, group them by origin, and print the mean sales figure and mean price.

## Reading the saved run

HKTV prints sales as a floor (`100+`, `5000+`). The **Number of sales** column stores that floor, so it is the number shown on the site, not an exact unit count.

Means for steak rows in the saved output:

| Steak category | Mean sales figure | Mean price (HKD) |
| --- | ---: | ---: |
| American | 372 | 134 |
| Australian | 197 | 181 |
| Japanese | 218 | 219 |
| New Zealand | 3,968 | 156 |
| Other | 1,666 | 168 |

New Zealand’s mean is high because a few listings show very large sales floors. **Other** is every steak whose name did not match a country keyword.

## Notes

- The scrape cell fills `granditemlistName`, `granditemlistPrice`, and `granditemlistSold`, then tries to clean `newitemlistSold`. That name is created in the next section, so a fresh kernel raises `NameError` on those last lines. The lists from the loop are already in memory; continue from **Store variables**. The same cleaning runs again under **Edit Variables**.
- The Wagyu summary filters `Product Type == "Steaks"`. The column value is `Steak`, so that grouping is empty. The first line of that cell is also cut off (`tableofsteaks["Wagy`). Delete that line and filter on `"Steak"` if you want the count. `count()` counts every row in the group, including rows where `Wagyu?` is `False`.
- HKTV’s class names and the Next button id can change. If the wait times out or the lists come back empty, those selectors in the scrape cell need an update.
- A consent or region dialog can sit on top of **Next**. Close it before the loop starts.
- Run the scrape cell once per session. It clears the grand lists at the start, then appends one page at a time.
