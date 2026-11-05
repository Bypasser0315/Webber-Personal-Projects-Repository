"""Short live smoke test for the Cookie Clicker automater.

Run: python run_smoke_test.py
"""

from __future__ import annotations

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOCKED_PRICE = 10**30


def parse_cookie_count(text: str) -> int:
    raw = text.split(" ")[0].replace(",", "").strip()
    return int(float(raw or "0"))


def parse_price(text: str) -> float:
    raw = text.replace(",", "").strip()
    if not raw:
        return LOCKED_PRICE
    try:
        return float(raw)
    except ValueError:
        return LOCKED_PRICE


def main() -> None:
    options = Options()
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 25)

    def js_click(element) -> None:
        driver.execute_script("arguments[0].click();", element)

    try:
        driver.get("https://cookie-clicker2.com/")
        driver.execute_script(
            """
            document.querySelectorAll(
              'iframe[id^="aswift"], iframe[title="Advertisement"], #pxcelframe'
            ).forEach((el) => { el.style.display = 'none'; });
            """
        )

        game_frame = wait.until(EC.presence_of_element_located((By.ID, "iframehtml5")))
        driver.switch_to.frame(game_frame)
        nested = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(nested[0])
        wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))

        buildings = [
            ("productPrice0", "product0"),
            ("productPrice1", "product1"),
            ("productPrice2", "product2"),
            ("productPrice3", "product3"),
        ]

        clicks = buys = 0
        start = time.time()
        while time.time() - start < 12 and clicks < 100:
            js_click(driver.find_element(By.ID, "bigCookie"))
            clicks += 1
            cookies = parse_cookie_count(driver.find_element(By.ID, "cookies").text)
            for price_id, product_id in buildings:
                price = parse_price(driver.find_element(By.ID, price_id).text)
                if cookies >= price:
                    js_click(driver.find_element(By.ID, product_id))
                    buys += 1
                    cookies = parse_cookie_count(driver.find_element(By.ID, "cookies").text)

        owned = driver.find_element(By.ID, "productOwned0").text
        final = driver.find_element(By.ID, "cookies").text.replace("\n", " | ")
        print(f"clicks={clicks} buys={buys} cursors={owned!r} final={final}")
        if clicks < 10 or buys < 1:
            raise SystemExit("Smoke test failed: expected clicks and at least one Cursor buy.")
        print("Smoke test OK")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
