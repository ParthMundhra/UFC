import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
from bs4 import BeautifulSoup
from database import SessionLocal
from models import Event

# FORCE logging to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

URL = "https://en.wikipedia.org/wiki/List_of_UFC_events"


def scrape_events():
    logger.info("Scraper started")

    db = SessionLocal()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links that look like UFC event pages
    links = soup.find_all("a", href=True)

    added = 0
    seen = set()

    for link in links:
        href = link["href"]

        if not href.startswith("/wiki/UFC_"):
            continue

        if ":" in href:  # skip special pages
            continue

        name = link.text.strip()
        if not name.startswith("UFC"):
            continue

        if name in seen:
            continue
        seen.add(name)

        wiki_url = "https://en.wikipedia.org" + href

        exists = db.query(Event).filter(Event.name == name).first()
        if exists:
            continue

        db.add(Event(
            name=name,
            date=None,
            location=None,
            wiki_url=wiki_url,
        ))
        added += 1

    db.commit()
    db.close()

    logger.info(f"Scraper finished. Added {added} events")
