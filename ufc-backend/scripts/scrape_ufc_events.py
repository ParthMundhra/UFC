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

from datetime import datetime
from bs4 import BeautifulSoup

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

def fight_exists(db: Session, red_id, blue_id, event):
    return (
        db.query(Fight)
        .filter(
            Fight.fighter_red == red_id,
            Fight.fighter_blue == blue_id,
            Fight.event == event
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

inserted = 0

for f in fights:
    red_fighter = get_or_create_fighter(db, f["red"])
    blue_fighter = get_or_create_fighter(db, f["blue"])

    if fight_exists(db, red_fighter.id, blue_fighter.id, f["event"]):
        continue

    fight = Fight(
    fighter_red=red_fighter.id,
    fighter_blue=blue_fighter.id,
    winner=red_fighter.id,
    method=f["method"],
    round=f["round"],
    event=f["event"],
    fight_date=event_date
    )


    db.add(fight)
    inserted += 1

db.commit()
db.close()

print(f"\nInserted {inserted} new fights into database")
