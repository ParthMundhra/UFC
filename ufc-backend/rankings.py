from sqlalchemy.orm import Session
from models import Fight, Fighter
from collections import defaultdict

def score_fight(method: str):
    method = (method or "").lower()
    if "ko" in method or "tko" in method:
        return 6
    if "submission" in method:
        return 5
    if "decision" in method:
        return 2
    return 0


MIN_FIGHTS = 2

def division_rankings(db: Session, division: str):
    total_points = defaultdict(int)
    fight_counts = defaultdict(int)

    fights = (
        db.query(Fight)
        .filter(Fight.division == division)
        .all()
    )

    for fight in fights:
        winner = fight.winner
        points = 10 + score_fight(fight.method)

# 5-round fight bonus
        if fight.round == 5:
            points += 2

        total_points[winner] += points
        fight_counts[winner] += 1

        fight_counts[winner] += 1

    rankings = []
    for fighter_id in total_points:
        if fight_counts[fighter_id] < MIN_FIGHTS:
            continue

        fighter = db.query(Fighter).get(fighter_id)
        avg_score = total_points[fighter_id] / fight_counts[fighter_id]

        rankings.append({
        "fighter": fighter.name,
        "avg_score": round(avg_score, 2),
        "fights": fight_counts[fighter_id],
        "total_points": total_points[fighter_id]
    })


    rankings.sort(key=lambda x: x["avg_score"], reverse=True)
    return rankings
