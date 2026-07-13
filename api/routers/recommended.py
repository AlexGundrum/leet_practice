import json
from datetime import date
from pathlib import Path

from fastapi import APIRouter

from api import storage

router = APIRouter(prefix="/api", tags=["recommended"])

ALGORITHMS_JSON_PATH = Path(__file__).resolve().parent.parent.parent / "algorithms.json"


def _weakest_category(ratings: dict):
    if not ratings:
        return None
    return min(ratings.items(), key=lambda kv: kv[1]["rating"])[0]


@router.get("/recommended-session")
def get_recommended_session():
    ratings = storage.read_json("elo/ratings.json", {})
    weakest = _weakest_category(ratings)

    atomic_drills = []
    specimens = []
    if weakest:
        with ALGORITHMS_JSON_PATH.open("r", encoding="utf-8") as f:
            algorithms = json.load(f)
        needle = weakest.lower().replace(" ", "_")
        atomic_drills = [
            {"id": a["id"], "title": a["title"], "difficulty": a["difficulty"]}
            for a in algorithms
            if needle in a["id"].lower() or weakest.lower() in a["title"].lower()
        ][:3]

        all_specimens = storage.read_json("specimen_problems.json", [])
        specimens = [
            s for s in all_specimens
            if s.get("pattern_tag") == weakest or weakest in s.get("tags", [])
        ][:3]

    today = date.today().isoformat()
    flashcards = storage.read_json("flashcards.json", [])
    due_flashcards = sorted(
        (c for c in flashcards if c["next_review_date"] <= today),
        key=lambda c: c["next_review_date"],
    )

    edge_cases = storage.read_json("edge_cases.json", [])
    due_edge_cases = sorted(
        (e for e in edge_cases if e["next_review_date"] <= today),
        key=lambda e: e["next_review_date"],
    )

    return {
        "weakest_category": weakest,
        "atomic_drills": atomic_drills,
        "specimens": specimens,
        "due_flashcards": due_flashcards,
        "due_edge_cases": due_edge_cases,
    }
