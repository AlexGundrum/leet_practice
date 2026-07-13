import json
import time
from pathlib import Path

from fastapi import APIRouter, HTTPException

from api import storage
from api.models import Attempt, CustomAlgorithm, LegacyImportPayload, Playlist

router = APIRouter(prefix="/api", tags=["practice"])

ALGORITHMS_JSON_PATH = Path(__file__).resolve().parent.parent.parent / "algorithms.json"
MIGRATED_MARKER = "migrated.json"  # stored under data/, via storage helpers below


@router.get("/algorithms")
def get_algorithms():
    with ALGORITHMS_JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/custom-algorithms")
def get_custom_algorithms():
    return storage.read_json("custom_algorithms.json", [])


@router.post("/custom-algorithms")
def add_custom_algorithm(algo: CustomAlgorithm):
    algos = storage.read_json("custom_algorithms.json", [])
    if any(a["id"] == algo.id for a in algos):
        raise HTTPException(status_code=409, detail="An algorithm with this ID already exists.")
    algos.append(algo.model_dump(exclude_none=True))
    storage.write_json("custom_algorithms.json", algos)
    return algo


@router.get("/attempts")
def get_attempts():
    return storage.read_json("attempts.json", [])


@router.post("/attempts")
def add_attempt(attempt: Attempt):
    attempts = storage.read_json("attempts.json", [])
    attempts.append(attempt.model_dump())
    storage.write_json("attempts.json", attempts)

    if attempt.passed:
        bests = storage.read_json("personal_bests.json", {})
        current = bests.get(attempt.algorithm_id)
        if not current or attempt.time_taken_ms < current["best_time_ms"]:
            bests[attempt.algorithm_id] = {
                "best_time_ms": attempt.time_taken_ms,
                "attempt_count": (current["attempt_count"] + 1) if current else 1,
                "first_passed_at": current["first_passed_at"] if current else attempt.timestamp,
            }
        else:
            current["attempt_count"] += 1
        storage.write_json("personal_bests.json", bests)

    return attempt


@router.get("/personal-bests")
def get_personal_bests():
    return storage.read_json("personal_bests.json", {})


@router.delete("/attempts")
def clear_attempts():
    storage.write_json("attempts.json", [])
    storage.write_json("personal_bests.json", {})
    return {"cleared": True}


@router.get("/playlists")
def get_playlists():
    return storage.read_json("playlists.json", [])


@router.put("/playlists")
def replace_playlists(playlists: list[Playlist]):
    storage.write_json("playlists.json", [p.model_dump() for p in playlists])
    return playlists


@router.post("/migrate/import-legacy")
def import_legacy(payload: LegacyImportPayload):
    if storage.read_json(MIGRATED_MARKER, None) is not None:
        raise HTTPException(status_code=409, detail="Legacy data has already been imported once.")

    storage.write_json("attempts.json", payload.attempts)
    storage.write_json("personal_bests.json", payload.personal_bests)
    storage.write_json("custom_algorithms.json", payload.custom_algorithms)
    storage.write_json("playlists.json", payload.playlists)
    storage.write_json(MIGRATED_MARKER, {"migrated_at": int(time.time() * 1000)})

    return {
        "attempts": len(payload.attempts),
        "custom_algorithms": len(payload.custom_algorithms),
        "playlists": len(payload.playlists),
    }
