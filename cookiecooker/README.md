# Cookie Clicker Automater

This is a small Selenium project that plays Cookie Clicker for you.

It opens [cookie-clicker2.com]([https://cookie-clicker2.com/#google_vignette]), clicks the big cookie over and over, and buys the first four buildings when you can afford them:

1. Cursor  
2. Grandma  
3. Farm  
4. Mine  

I built this to practise browser automation with Python and Selenium. It is a learning project, not a full Cookie Clicker bot.

## Cookie Clicker

The game works by clicking a cookie, which grants a cookie. With enough cookies, upgrades can be purchased, which increases the number of cookies generated per click or adds automated cursors that click the cookie for the user. 

Here is a screenshot of the game while the Automater is running: 

<img width="1361" height="787" alt="Screenshot 2026-11-03 181612" src="https://github.com/user-attachments/assets/9445a2ad-6d95-4062-9597-d2d374fa51ed" />

A short video of the cookie clicker automater running can be found in this youtube link: 
https://youtu.be/G2MJwQQ2yag

## What you need

- Python 3
- Google Chrome
- Selenium

```bash
pip install selenium
```

## How to run

### Option A — notebook

1. Open `autocookieclicker.ipynb`.
2. Run the cells from top to bottom.
3. When Chrome opens, accept any consent popup if one appears.
4. Run **Setup**, then **Start Automation**.
5. Stop with **Kernel → Interrupt**.

### Option B — short smoke test

This runs a quick live check (about 100 clicks) and then exits:

```bash
cd cookiecooker
python run_smoke_test.py
```

You should see it buy a few Cursors and print `Smoke test OK`.

## What’s in this folder

| File | Purpose |
| --- | --- |
| `autocookieclicker.ipynb` | Main notebook — open the game, set up, automate |
| `run_smoke_test.py` | Short script to confirm the bot still works on the live site |
| `README.md` | This file |

## How it works

The Cookie Clicker mirror puts the real game inside nested iframes. The notebook:

1. Opens the site in Chrome
2. Hides common ad iframes so they do not block clicks
3. Switches into `#iframehtml5`, then the nested game iframe
4. Finds `#bigCookie` and building buttons `product0`–`product3`
5. Clicks the cookie in a loop and buys a building whenever your cookie count covers the price

Clicks are done with JavaScript (`element.click()` via Selenium’s script runner). On this site, normal Selenium clicks are often blocked by ads sitting on top of the game.

## Tips

- If **Setup** fails, refresh the page, close popups/ads, and run Setup again.
- Only the first four buildings are handled.
- Leave the Chrome window alone while the loop is running.
- Prices that are blank or locked are treated as “too expensive,” so the bot skips them.

## Notes

This uses a third-party Cookie Clicker mirror, so ads and iframe layout can change. If the site redesigns its embed, the frame-switching step may need another update.
