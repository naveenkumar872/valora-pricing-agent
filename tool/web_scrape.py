from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

# ✅ New Flipkart price class
PRICE_CLASS = "Nx9bqj"

def extract_discounted_prices_only(html):
    soup = BeautifulSoup(html, "html.parser")
    prices = []

    for tag in soup.find_all("div", class_=PRICE_CLASS):
        price_text = tag.get_text(strip=True).replace("₹", "").replace(",", "")
        if price_text.isdigit():
            prices.append(int(price_text))

    print(f"✅ Found {len(prices)} raw prices from HTML.")
    unique_prices = sorted(set(prices))
    print(f"🔁 Final unique prices (₹): {unique_prices}")
    return unique_prices

def scrape_flipkart_prices(query: str,page : int):
    print(f"\n🔎 Scrolling Flipkart for query: '{query}'")

    options = Options()
    # options.add_argument("--headless")  # enable for silent scraping
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1200")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(), options=options)

    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}&sort=price_asc&page={page}"
    print(f"🌐 Opening URL: {url}")
    driver.get(url)
    time.sleep(3)

    # ✅ Try closing login popup
    try:
        close_btn = driver.find_element(By.XPATH, "//button[contains(text(), '✕')]")
        close_btn.click()
        print("✅ Login popup closed")
        time.sleep(1)
    except:
        print("ℹ️ No login popup")

    # ✅ Scroll multiple times to load content
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       
    time.sleep(2)

    # ✅ Wait until price class is detected in page source
    try:
        WebDriverWait(driver, 10).until(lambda d: PRICE_CLASS in d.page_source)
        print(f"🟢 Price class '{PRICE_CLASS}' found")
    except:
        print(f"⚠️ Price class '{PRICE_CLASS}' NOT found in time")

    # ✅ Save HTML
    html = driver.page_source
    with open("flipkart_dump.html", "w", encoding="utf-8") as f:
        f.write(html)
        print("📝 HTML saved to flipkart_dump_scroll.html")

    driver.quit()

    # ✅ Extract prices from soup
    return extract_discounted_prices_only(html)

