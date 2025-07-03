from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

def extract_all_prices_from_html(html):
    matches = re.findall(r'₹\s?[\d,]+', html)
    prices = []
    for match in matches:
        price = match.replace("₹", "").replace(",", "").strip()
        if price.isdigit():
            prices.append(int(price))
    return prices

def scrape_flipkart_prices(query="red tshirt"):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1200")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(), options=options)
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(3)

    try:
        close_btn = driver.find_element(By.XPATH, "//button[contains(text(), '✕')]")
        close_btn.click()
        print("✅ Login popup closed")
        time.sleep(1)
    except:
        print("ℹ️ No login popup")

    html = driver.page_source
    with open("flipkart_dump.html", "w", encoding="utf-8") as f:
        f.write(html)
        print("📝 HTML saved to flipkart_dump.html")

    driver.quit()

    # ✅ Extract ₹ prices with regex
    prices = extract_all_prices_from_html(html)
    print(f"🔎 Flipkart Prices for '{query}':", prices[:10])
    return prices[:10]
