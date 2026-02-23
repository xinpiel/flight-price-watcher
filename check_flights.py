import os
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Telegram secrets (from GitHub Actions)
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Flight configuration
ORIGIN = "AMS"

DESTINATIONS = {
    "Beijing": "PEK",
    "Shanghai": "PVG",
    "Guangzhou": "CAN",
    "Shenzhen": "SZX",
    "Chengdu": "CTU",
    "Xiamen": "XMN"
}

DEPART_DATE = "2026-07-17"
RETURN_DATE = "2026-08-29"

DB = "prices.db"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": text},
        timeout=10
    )


def get_price(destination_code):
    url = (
        f"https://www.skyscanner.net/transport/flights/"
        f"{ORIGIN}/{destination_code}/"
        f"{DEPART_DATE}/{RETURN_DATE}/"
    )

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=25)
    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.select_one('[data-test-id="price-main"]')
    if not price_tag:
        return None

    return int("".join(filter(str.isdigit, price_tag.text)))


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            timestamp TEXT,
            destination TEXT,
            price INTEGER
        )
    """)

    for city, code in DESTINATIONS.items():
        price = get_price(code)
        if price is None:
            continue

        c.execute(
            "SELECT MIN(price) FROM prices WHERE destination = ?",
            (code,)
        )
        best_price = c.fetchone()[0]

        c.execute(
            "INSERT INTO prices VALUES (?, ?, ?)",
            (datetime.utcnow().isoformat(), code, price)
        )
        conn.commit()

        if best_price is None or price < best_price:
            send_message(
                f"✈️ NEW LOW PRICE!\n"
                f"AMS → {city}\n"
                f"{DEPART_DATE} → {RETURN_DATE}\n"
                f"New price: €{price}\n"
                f"Previous best: {best_price or 'N/A'}"
            )

    conn.close()


if __name__ == "__main__":
    main()
