from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api import srs_engine, storage

router = APIRouter(prefix="/api/edge-cases", tags=["edge_cases"])


class ReviewResult(BaseModel):
    remembered: bool


EDGE_CASE_MASTERY_THRESHOLD_DAYS = 14


@router.get("/due")
def get_due_edge_cases():
    edge_cases = storage.read_json("edge_cases.json", [])
    today = date.today().isoformat()
    due = [e for e in edge_cases if e["next_review_date"] <= today]
    due = [
        e for e in due
        if srs_engine.should_include_due_card(e.get("interval_days", 0), EDGE_CASE_MASTERY_THRESHOLD_DAYS)
    ]
    due.sort(key=lambda e: e["next_review_date"])
    return due


@router.post("/{edge_case_id}/review")
def review_edge_case(edge_case_id: str, body: ReviewResult):
    edge_cases = storage.read_json("edge_cases.json", [])
    idx = next((i for i, e in enumerate(edge_cases) if e["id"] == edge_case_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Edge case '{edge_case_id}' not found.")

    edge_cases[idx] = srs_engine.review_edge_case(edge_cases[idx], body.remembered)
    storage.write_json("edge_cases.json", edge_cases)
    return edge_cases[idx]
