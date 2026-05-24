from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import os

# --- CONFIGURATION --- (reads from environment variables now)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MEMORY_FILE = "seen_items.txt"

# --- TELEGRAM NOTIFIER ---
def notify_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        import requests
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
        print("✅ Telegram notification sent!")
    except Exception as e:
        print(f"❌ Failed to connect to Telegram: {e}")

# --- MEMORY SYSTEM ---
def load_seen_items():
    if not os.path.exists(MEMORY_FILE): return set()
    with open(MEMORY_FILE, "r") as file: return set(line.strip() for line in file.readlines())

def save_current_stock(current_in_stock_list):
    with open(MEMORY_FILE, "w") as file:
        for item_id in current_in_stock_list: file.write(f"{item_id}\n")

# --- THE SCRAPER ---
def check_firstcry():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Launching browser to scrape all items...")
    
    url = 'https://www.firstcry.com/hotwheels/5/0/113'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        
        for _ in range(15): 
            page.evaluate("window.scrollBy(0, 1500)")
            time.sleep(1)
        
        html = page.content()
        browser.close()
        
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all('div', class_='list_block')
        
        print(f"Found {len(products)} products on page.")
        
        seen_items = load_seen_items()
        current_in_stock = set()
        new_items_found = 0
        
        for product in products:
            try:
                title_div = product.find('div', class_='li_txt1')
                if not title_div or not title_div.find('a'):
                    continue
                
                anchor = title_div.find('a')
                item_name = anchor.get('title', 'Unknown Item')
                item_url = anchor.get('href', '')
                full_url = f"https://www.firstcry.com{item_url}" if item_url.startswith('/') else item_url
                
                star_div = product.find('div', class_='star')
                item_id = star_div.get('data-val') if star_div else None
                
                is_in_stock = product.find('div', class_='ga_bn_btn_addcart') is not None
                
                if item_id and is_in_stock:
                    current_in_stock.add(item_id)
                    if item_id not in seen_items:
                        print(f"🚨 NEW RESTOCK: {item_name}")
                        notify_telegram(f"🚨 New Restock: {item_name}\n\nLink: {full_url}")
                        new_items_found += 1
                        
            except Exception as e:
                print(f"Error parsing a product card: {e}")
                
        save_current_stock(current_in_stock)
        print(f"Cycle complete. Found {len(current_in_stock)} items in stock.")

# ✅ CHANGED: No while loop needed — GitHub Actions handles the scheduling
if __name__ == "__main__":
    print("Starting FirstCry Tracker (GitHub Actions run)...")
    check_firstcry()
