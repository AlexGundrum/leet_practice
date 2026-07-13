from typing import Optional

from fastapi import APIRouter

from api import storage

router = APIRouter(prefix="/api/elo", tags=["elo"])


@router.get("")
def get_ratings():
    return storage.read_json("elo/ratings.json", {})


@router.get("/history")
def get_history(category: Optional[str] = None):
    rows = storage.read_jsonl("elo/history.jsonl")
    if category:
        rows = [r for r in rows if r["category"] == category]
    return rows
