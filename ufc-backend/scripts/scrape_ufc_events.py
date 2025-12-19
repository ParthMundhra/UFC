import sys
import os

# Add ufc-backend root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import requests
import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Fighter, Fight
from models import Event, Fight

from datetime import datetime
from bs4 import BeautifulSoup

import re

def clean_fighter_name(name: str):
    return re.sub(r"\s*\(.*?\)", "", name).strip()

EVENTS = [
    # Recent PPVs
    {
        "name": "UFC 282",
        "url": "https://en.wikipedia.org/wiki/UFC_282"
    },
    {
        "name": "UFC 283",
        "url": "https://en.wikipedia.org/wiki/UFC_283"
    },

    # Recent Fight Nights
    {
        "name": "UFC Fight Night: Vera vs. Cruz",
        "url": "https://en.wikipedia.org/wiki/UFC_on_ESPN:_Vera_vs._Cruz"
    },
    {
        "name": "UFC Fight Night: Kattar vs. Allen",
        "url": "https://en.wikipedia.org/wiki/UFC_Fight_Night:_Kattar_vs._Allen"
    },
    {
        "name": "UFC Fight Night: Grasso vs. Araújo",
        "url": "https://en.wikipedia.org/wiki/UFC_Fight_Night:_Grasso_vs._Ara%C3%BAjo"
    }
]


def get_or_create_event(db: Session, name: str, date=None):
    event = db.query(Event).filter(Event.name == name).first()
    if event:
        return event

    event = Event(
        name=name,
        date=date
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def scrape_event(url: str, event_name: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html = response.text

    event_date = extract_event_date(html)

    tables = pd.read_html(StringIO(html))
    df = tables[2]  # Main card table (modern events)

    # Flatten multi-index columns
    df.columns = [col[1] for col in df.columns]

    fights = []

    for _, row in df.iterrows():
        red = clean_fighter_name(str(row["Unnamed: 1_level_1"]))
        blue = clean_fighter_name(str(row["Unnamed: 3_level_1"]))

        round_ = row["Round"]
        if not str(round_).isdigit():
            continue
        
        division = str(row["Weight class"]).strip()

        fights.append({
        "red": red,
        "blue": blue,
        "method": row["Method"],
        "round": int(round_),
        "time": row["Time"],
        "event": event_name,
        "date": event_date,
        "division": division
    })
    return fights


def extract_event_date(html):
    soup = BeautifulSoup(html, "html.parser")

    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return None

    for row in infobox.find_all("tr"):
        header = row.find("th")
        if header and "Date" in header.text:
            date_text = row.find("td").text.strip()
            # Example: "October 22, 2022"
            try:
                return datetime.strptime(date_text, "%B %d, %Y").date()
            except:
                return None

    return None


def get_or_create_fighter(db: Session, name: str):
    fighter = db.query(Fighter).filter(Fighter.name == name).first()
    if fighter:
        return fighter

    fighter = Fighter(
        name=name,
        wins=0,
        losses=0,
        division=None
    )
    db.add(fighter)
    db.commit()
    db.refresh(fighter)
    return fighter

def fight_exists(db: Session, red_id, blue_id, event, round_):
    return (
        db.query(Fight)
        .filter(
            Fight.fighter_red == red_id,
            Fight.fighter_blue == blue_id,
            Fight.event == event,
            Fight.round == round_
        )
        .first()
        is not None
    )



URL = "https://en.wikipedia.org/wiki/UFC_280"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

html = response.text
event_date = extract_event_date(html)
print("Event date:", event_date)


tables = pd.read_html(StringIO(html))

# TABLE 2 is the Main card fights
df = tables[2]

# Flatten multi-level columns
df.columns = [col[1] for col in df.columns]

fights = []

for _, row in df.iterrows():
    # Fighter names are in the unnamed columns
    red = str(row["Unnamed: 1_level_1"]).strip()
    blue = str(row["Unnamed: 3_level_1"]).strip()

    method = row["Method"]
    round_ = row["Round"]

# Skip section headers like "Preliminary card"
    if not str(round_).isdigit():
        continue

    time = row["Time"]

    if pd.isna(red) or pd.isna(blue):
        continue

    fights.append({
        "red": red,
        "blue": blue,
        "method": method,
        "round": int(round_),
        "time": time,
        "event": "UFC 280"
    })

for f in fights:
    print(f)

print(f"\nTotal fights extracted: {len(fights)}")

db = SessionLocal()
total_inserted = 0

for event in EVENTS:
    print(f"\nScraping {event['name']}...")

    try:
        fights = scrape_event(event["url"], event["name"])
    except Exception as e:
        print(f"❌ Failed to scrape {event['name']}: {e}")
        continue


    # ✅ PHASE 2: ensure event exists
    event_obj = get_or_create_event(
        db,
        name=event["name"],
        date=fights[0]["date"] if fights else None
    )

    for f in fights:
        red_fighter = get_or_create_fighter(db, f["red"])
        blue_fighter = get_or_create_fighter(db, f["blue"])

        if fight_exists(
        db,
        red_fighter.id,
        blue_fighter.id,
        f["event"],
        f["round"]
    ):
            continue


        fight = Fight(
            fighter_red=red_fighter.id,
            fighter_blue=blue_fighter.id,
            winner=red_fighter.id,
            method=f["method"],
            round=f["round"],
            event=event_obj.name,   # 🔑 event-aware
            fight_date=f["date"],
            division=f["division"]
        )

        db.add(fight)
        total_inserted += 1


db.commit()
db.close()

print(f"\nTOTAL fights inserted: {total_inserted}")



