from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from dotenv import load_dotenv
import os
import requests
import urllib.parse

from database import engine, get_db
from models import Base, Fighter, Fight, Event
from rankings import division_rankings

# ---------------- SETUP ----------------

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ✅ allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# ---------------- ROOT ----------------

@app.get("/")
def home():
    return {"message": "UFC API running"}

# ---------------- FIGHT EXPLORER (OPTION A CORE) ----------------

@app.get("/fights")
def get_fights(
    event: str | None = None,
    db: Session = Depends(get_db)
):
    query = (
        db.query(Fight)
        .options(
            joinedload(Fight.red_fighter),
            joinedload(Fight.blue_fighter),
            joinedload(Fight.winner_fighter),
        )
    )

    if event:
        query = query.filter(Fight.event == event)

    fights = query.all()

    return [
        {
            "red": f.red_fighter.name if f.red_fighter else "Unknown",
            "blue": f.blue_fighter.name if f.blue_fighter else "Unknown",
            "winner": f.winner_fighter.name if f.winner_fighter else None,
            "method": f.method,
            "round": f.round,
            "division": f.division,
            "event": f.event,
        }
        for f in fights
    ]

# ---------------- EVENTS (FOR FILTER DROPDOWN) ----------------

@app.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.name.desc()).all()
    return [{"name": e.name, "date": e.date} for e in events]

# ---------------- RANKINGS ----------------

@app.get("/rankings/division/{division}")
def get_division_rankings(division: str, db: Session = Depends(get_db)):
    return division_rankings(db, division)

# ---------------- FIGHTER PROFILE ----------------

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
        .options(
            joinedload(Fight.red_fighter),
            joinedload(Fight.blue_fighter),
            joinedload(Fight.winner_fighter),
        )
        .all()
    )

    wins = sum(1 for f in fights if f.winner == fighter.id)
    losses = len(fights) - wins

    finish_wins = 0
    decision_wins = 0

    for f in fights:
        if f.winner == fighter.id:
            if "Decision" in f.method:
                decision_wins += 1
            else:
                finish_wins += 1


    history = []
    for f in fights:
        opponent = (
            f.blue_fighter if f.red_fighter.id == fighter.id
            else f.red_fighter
        )

        history.append({
            "opponent": opponent.name if opponent else "Unknown",
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
        "finish_wins": finish_wins,
        "decision_wins": decision_wins,
        "history": history,
        "finish_rate": round(
    (finish_wins / wins) * 100, 1
) if wins > 0 else 0
    }

# ---------------- NEWS ----------------

@app.get("/news")
def ufc_news():
    if not GNEWS_API_KEY:
        return []

    url = "https://gnews.io/api/v4/search"
    params = {
        "q": "UFC OR MMA",
        "lang": "en",
        "country": "us",
        "max": 6,
        "apikey": GNEWS_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    return [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "image": a["image"],
            "url": a["url"],
        }
        for a in data.get("articles", [])
    ]

# ---------------- FIGHTER IMAGE ----------------

@app.get("/fighter-image/{name}")
def fighter_image(name: str):
    formatted = urllib.parse.quote(name.replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted}"

    try:
        r = requests.get(url, timeout=3).json()
        return {"image": r.get("thumbnail", {}).get("source")}
    except:
        return {"image": None}
