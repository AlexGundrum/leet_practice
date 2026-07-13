from typing import Optional

from fastapi import APIRouter, HTTPException

from api import storage

router = APIRouter(prefix="/api", tags=["specimens"])


@router.get("/specimen-proposals")
def list_proposals():
    return storage.read_json("specimen_proposals.json", [])


@router.post("/specimen-proposals/{proposal_id}/approve")
def approve_proposal(proposal_id: str):
    proposals = storage.read_json("specimen_proposals.json", [])
    idx = next((i for i, p in enumerate(proposals) if p["id"] == proposal_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Proposal '{proposal_id}' not found.")

    proposal = proposals.pop(idx)
    specimens = storage.read_json("specimen_problems.json", [])
    specimens.append({
        "id": proposal["id"],
        "title": proposal["title"],
        "tags": proposal["patterns"],
        "difficulty": "medium",
        "stub": None,
        "test_cases": [],
        "description": None,
        "solution_code": proposal["solution_code"],
        "solution_explanation": proposal["reason"],
        "when_to_use": None,
        "source_contest": proposal["source_contest"],
        "pattern_tag": proposal["patterns"][0] if proposal["patterns"] else "",
        "date": proposal["date"],
    })

    storage.write_json("specimen_proposals.json", proposals)
    storage.write_json("specimen_problems.json", specimens)
    return {"approved": True, "specimen": specimens[-1]}


@router.post("/specimen-proposals/{proposal_id}/reject")
def reject_proposal(proposal_id: str):
    proposals = storage.read_json("specimen_proposals.json", [])
    idx = next((i for i, p in enumerate(proposals) if p["id"] == proposal_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Proposal '{proposal_id}' not found.")

    proposals.pop(idx)
    storage.write_json("specimen_proposals.json", proposals)
    return {"rejected": True}


@router.get("/specimen-problems")
def list_specimen_problems(pattern_tag: Optional[str] = None):
    specimens = storage.read_json("specimen_problems.json", [])
    if pattern_tag:
        specimens = [s for s in specimens if s.get("pattern_tag") == pattern_tag]
    return specimens
