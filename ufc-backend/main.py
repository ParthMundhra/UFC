from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Fighter
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

import os
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "UFC API with DB is running"}

@app.get("/fighters")
def get_fighters(db: Session = Depends(get_db)):
    return db.query(Fighter).all()


from models import Fight
from sqlalchemy.orm import Session

@app.get("/fights")
def get_fights(db: Session = Depends(get_db)):
    fights = db.query(Fight).all()
    return [
        {
            "id": fight.id,
            "event": fight.event,
            "date": fight.fight_date,
            "red_corner": fight.red_fighter.name if fight.red_fighter else None,
            "blue_corner": fight.blue_fighter.name if fight.blue_fighter else None,
            "winner": fight.winner_fighter.name if fight.winner_fighter else None,
            "method": fight.method,
            "round": fight.round,
        }
        for fight in fights
    ]

from rankings import division_rankings

@app.get("/rankings/division/{division}")
def get_division_rankings(division: str, db: Session = Depends(get_db)):
    return division_rankings(db, division)

@app.get("/fighters/{fighter_name}")
def fighter_profile(fighter_name: str, db: Session = Depends(get_db)):
    fighter = db.query(Fighter).filter(Fighter.name == fighter_name).first()
    if not fighter:
        return {"error": "Fighter not found"}

    fights = (
        db.query(Fight)
        .filter(
            (Fight.fighter_red == fighter.id) |
            (Fight.fighter_blue == fighter.id)
        )
        .all()
    )

    wins = sum(1 for f in fights if f.winner == fighter.id)
    losses = len(fights) - wins

    history = []
    for f in fights:
        opponent_id = f.fighter_blue if f.fighter_red == fighter.id else f.fighter_red
        opponent = db.query(Fighter).get(opponent_id)

        history.append({
            "opponent": opponent.name,
            "result": "Win" if f.winner == fighter.id else "Loss",
            "method": f.method,
            "event": f.event,
            "division": f.division,
        })

    return {
        "name": fighter.name,
        "wins": wins,
        "losses": losses,
        "total_fights": len(fights),
        "history": history
    }

@app.get("/events")
def list_events(db: Session = Depends(get_db)):
    events = db.query(Fight.event).distinct().all()
    return sorted([e[0] for e in events])


@app.get("/fights/event/{event_name}")
def fights_by_event(event_name: str, db: Session = Depends(get_db)):
    fights = db.query(Fight).filter(Fight.event == event_name).all()

    result = []
    for f in fights:
        red = db.query(Fighter).get(f.fighter_red)
        blue = db.query(Fighter).get(f.fighter_blue)
        winner = db.query(Fighter).get(f.winner)

        result.append({
            "red": red.name,
            "blue": blue.name,
            "winner": winner.name,
            "method": f.method,
            "round": f.round,
            "division": f.division
        })

    return result


import requests
from fastapi import Query

GNEWS_API_KEY = "b7fe53a17eba72409d13ce8a9809f9fe"

@app.get("/news")
def ufc_news():
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": "UFC OR MMA",
        "lang": "en",
        "country": "us",
        "max": 6,
        "apikey": GNEWS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []
    for a in data.get("articles", []):
        articles.append({
            "title": a["title"],
            "source": a["source"]["name"],
            "image": a["image"],
            "url": a["url"]
        })

    return articles

import urllib.parse

@app.get("/fighter-image/{name}")
def fighter_image(name: str):
    formatted = urllib.parse.quote(name.replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted}"

    try:
        r = requests.get(url, timeout=3).json()
        return {"image": r.get("thumbnail", {}).get("source")}
    except:
        return {"image": None}
