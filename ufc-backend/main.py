from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Fighter
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

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


