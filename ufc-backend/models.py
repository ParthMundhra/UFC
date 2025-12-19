from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from database import Base
Base = declarative_base()

class Fighter(Base):
    __tablename__ = "fighters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nickname = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    division = Column(String)


class Fight(Base):
    __tablename__ = "fights"

    id = Column(Integer, primary_key=True, index=True)
    fighter_red = Column(Integer, ForeignKey("fighters.id"))
    fighter_blue = Column(Integer, ForeignKey("fighters.id"))
    winner = Column(Integer, ForeignKey("fighters.id"))
    method = Column(String)
    round = Column(Integer)
    event = Column(String)
    fight_date = Column(Date)
    division = Column(String)


    red_fighter = relationship("Fighter", foreign_keys=[fighter_red])
    blue_fighter = relationship("Fighter", foreign_keys=[fighter_blue])
    winner_fighter = relationship("Fighter", foreign_keys=[winner])

from sqlalchemy import Column, Integer, String, Date
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    date = Column(String)        # keep String for now (Wikipedia formats vary)
    location = Column(String)
    wiki_url = Column(String, unique=True)

