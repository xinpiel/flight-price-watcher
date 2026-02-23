import os
import requests
from bs4 import BeautifulSoup
import sqlite3

# Telegram info from env
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

cities = {
    "Beijing": "PEK",
    "Shanghai": "SHA",
    "Guangzhou": "CAN",
    "Shenzhen": "SZX",
    "Chengdu": "CTU",
    "Xiamen": "XMN"
}

# Connect to local database
conn = sqlite3.connect("prices.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS prices
             (city TEXT PRIMARY KEY, price REAL)''')

def send_message(message):
    print(f"Attempting to send Telegram message: {message}")  # Debug print
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print(f"Telegram API response: {response.status_code}, {response.text}")  # Debug

def get_price(city_code):
    # Example scraping from Skyscanner (update if needed)
    url = f"https://www.skyscanner.com/transport/flights/ams/{city_code}/230717/290826/"
    print(f"Fetching URL: {url}")  # Debug
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Failed to fetch {city_code}, status: {r.status_code}")
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    price_tag = soup.select_one('[data-test-id="price-main"]')
    if price_tag:
        try:
            price = int("".join(filter(str.isdigit, price_tag.text)))
            return price
        except:
            print(f"Failed to parse price for {city_code}")
            return None
    else:
        print(f"No price found for {city_code}")
        return None

for city, code in cities.items():
    print(f"Checking {city} ({code})")  # Debug
    price = get_price(code)
    print(f"Price found: {price}")      # Debug

    # Check database
    c.execute("SELECT price FROM prices WHERE city=?", (city,))
    row = c.fetchone()
    best_price = row[0] if row else None

    if best_price is None or (price is not None and price < best_price):
        print(f"Sending Telegram message for {city}")  # Debug
        send_message(f"✈️ NEW LOW PRICE!\nAMS → {city}\nPrice: €{price}\nPrevious best: {best_price}")
        c.execute("REPLACE INTO prices (city, price) VALUES (?,?)", (city, price))
    else:
        print(f"No new low price for {city} (current: {price}, best: {best_price})")

conn.commit()
conn.close()
