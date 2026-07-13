from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api import srs_engine, storage

router = APIRouter(prefix="/api/flashcards", tags=["flashcards"])


class ReviewGrade(BaseModel):
    grade: Literal["again", "hard", "good", "easy"]


@router.get("/due")
def get_due_flashcards():
    cards = storage.read_json("flashcards.json", [])
    today = date.today().isoformat()
    due = [c for c in cards if c["next_review_date"] <= today]
    due = [c for c in due if srs_engine.should_include_due_card(c.get("interval_days", 0))]
    due.sort(key=lambda c: c["next_review_date"])
    return due


@router.post("/{card_id}/review")
def review_flashcard(card_id: str, body: ReviewGrade):
    cards = storage.read_json("flashcards.json", [])
    idx = next((i for i, c in enumerate(cards) if c["id"] == card_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Flashcard '{card_id}' not found.")

    cards[idx] = srs_engine.review_flashcard(cards[idx], body.grade)
    storage.write_json("flashcards.json", cards)
    return cards[idx]
