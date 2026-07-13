from fastapi import APIRouter

from api import pacing, storage

router = APIRouter(prefix="/api", tags=["pacing"])


@router.get("/pacing-status")
def get_pacing_status():
    contest_dates = storage.load_contest_dates()
    return pacing.pacing_status(contest_dates)
