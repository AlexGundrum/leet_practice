import json
import re
import time
import uuid
from datetime import date

from fastapi import APIRouter, HTTPException

from api import elo_engine, storage
from api.models import Contest, ContestMeta, GradingImport, ProblemCapture

router = APIRouter(prefix="/api/contests", tags=["contests"])


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "contest"


def _contest_path(contest_id: str) -> str:
    return f"contests/{contest_id}.json"


def _load_contest(contest_id: str) -> dict:
    contest = storage.read_json(_contest_path(contest_id), None)
    if contest is None:
        raise HTTPException(status_code=404, detail=f"Contest '{contest_id}' not found.")
    return contest


def _save_contest(contest_id: str, contest: dict) -> None:
    storage.write_json(_contest_path(contest_id), contest)


@router.post("")
def create_contest(meta: ContestMeta):
    contest_id = f"{meta.date}_{_slugify(meta.name)}"
    if storage.read_json(_contest_path(contest_id), None) is not None:
        contest_id = f"{contest_id}-{uuid.uuid4().hex[:6]}"

    contest = Contest(id=contest_id, meta=meta, problems=[]).model_dump()
    _save_contest(contest_id, contest)
    return contest


@router.get("")
def list_contests():
    summaries = []
    for path in storage.list_contest_files():
        contest = storage.read_json(f"contests/{path.name}", None)
        if contest is None:
            continue
        summaries.append({
            "id": contest["id"],
            "name": contest["meta"]["name"],
            "date": contest["meta"]["date"],
            "type": contest["meta"]["type"],
            "num_problems": len(contest.get("problems", [])),
            "graded": contest.get("grading_result") is not None,
        })
    summaries.sort(key=lambda c: c["date"], reverse=True)
    return summaries


@router.get("/{contest_id}")
def get_contest(contest_id: str):
    return _load_contest(contest_id)


@router.post("/{contest_id}/problems")
def upsert_problem(contest_id: str, problem: ProblemCapture):
    contest = _load_contest(contest_id)
    problems = contest.setdefault("problems", [])
    match_idx = next(
        (i for i, p in enumerate(problems) if p["title"].strip().lower() == problem.title.strip().lower()),
        None,
    )
    if match_idx is not None:
        problems[match_idx] = problem.model_dump()
    else:
        problems.append(problem.model_dump())
    _save_contest(contest_id, contest)
    return contest


GRADING_RUBRIC = """\
You are grading my LeetCode contest performance. I'm doing this reflection a day \
(or more) after the contest on purpose - I want you to critique my THINKING PROCESS, \
not just whether I got the right answer.

For each problem below, look at every submission I made (in order), my narrative of \
what I was thinking, and any failing test cases. Then return ONLY a single JSON object \
(no prose, no markdown fences) matching EXACTLY this shape:

{
  "contest_meta": {"name": "", "date": "", "type": "official|virtual", "problems_attempted": 0, "problems_solved": 0},
  "per_problem": [{
    "title": "",
    "patterns": ["e.g. binary_search, dp, greedy, graphs, intervals, ..."],
    "verdict": "solved|unsolved|solved_late",
    "difficulty": "easy|medium|hard - LeetCode's own difficulty rating for this problem",
    "submissions": [{"code": "", "verdict": "", "failing_test": "", "ai_note": "brief note on what this submission got wrong/right"}],
    "critique": {
      "thinking_process_score": "integer 1-5, 1=poor process 5=excellent process",
      "what_went_right": "",
      "what_went_wrong": "",
      "root_cause_of_delay": "be specific about which pattern/category was actually the root cause, if any"
    },
    "flashcards_generated": [{"front": "a generalizable question, not specific to this exact problem", "back": "", "tag": "pattern name"}],
    "edge_cases_missed": [{"category": "e.g. empty_input, off_by_one, integer_overflow, duplicates, negative_numbers", "description": "", "generalized_lesson": ""}],
    "specimen_candidate": {"propose": false, "reason": "only propose true if this problem is a particularly good illustration of a pattern worth remembering"}
  }],
  "overall_summary": {"strengths": "", "weaknesses": "", "recommended_focus_next_week": ""}
}

Here is the contest data:

"""


@router.get("/{contest_id}/grading-prompt")
def get_grading_prompt(contest_id: str):
    contest = _load_contest(contest_id)
    payload = {
        "contest_meta": contest["meta"],
        "problems": contest.get("problems", []),
    }
    prompt = GRADING_RUBRIC + json.dumps(payload, indent=2)
    return {"prompt": prompt}


@router.post("/{contest_id}/import-grading")
def import_grading(contest_id: str, grading: GradingImport):
    contest = _load_contest(contest_id)

    contest["grading_result"] = grading.model_dump()
    contest["grading_imported_at"] = int(time.time() * 1000)
    _save_contest(contest_id, contest)

    today = date.today().isoformat()
    added_flashcards = 0
    added_edge_cases = 0
    added_proposals = 0

    flashcards = storage.read_json("flashcards.json", [])
    edge_cases = storage.read_json("edge_cases.json", [])
    proposals = storage.read_json("specimen_proposals.json", [])
    ratings = storage.read_json("elo/ratings.json", {})
    updated_categories = []

    captured_by_title = {
        p["title"].strip().lower(): p for p in contest.get("problems", [])
    }

    for problem in grading.per_problem:
        solved = problem.verdict in ("solved", "solved_late")
        submission_count = len(problem.submissions)
        captured = captured_by_title.get(problem.title.strip().lower())
        time_to_solve_min = captured.get("time_to_solve_min") if captured else None
        s_obj = elo_engine.objective_score(solved, submission_count, time_to_solve_min, problem.difficulty)

        for pattern in problem.patterns:
            implicated = elo_engine.is_implicated(pattern, problem.critique.root_cause_of_delay)
            s_ai = elo_engine.ai_adjustment(implicated, problem.critique.thinking_process_score)

            current_state = ratings.get(pattern, {})
            new_state, history_extra = elo_engine.update_category_rating(
                current_state, s_obj, s_ai, problem.difficulty
            )
            new_state["last_updated"] = int(time.time() * 1000)
            ratings[pattern] = new_state

            storage.append_jsonl("elo/history.jsonl", {
                "ts": int(time.time() * 1000),
                "category": pattern,
                "contest_id": contest_id,
                "problem_title": problem.title,
                **history_extra,
            })
            updated_categories.append(pattern)
        for card in problem.flashcards_generated:
            flashcards.append({
                "id": uuid.uuid4().hex,
                "front": card.front,
                "back": card.back,
                "tag": card.tag,
                "contest_id": contest_id,
                "ease_factor": 2.5,
                "interval_days": 0,
                "repetitions": 0,
                "next_review_date": today,
                "last_reviewed_at": None,
            })
            added_flashcards += 1

        for ec in problem.edge_cases_missed:
            edge_cases.append({
                "id": uuid.uuid4().hex,
                "category": ec.category,
                "description": ec.description,
                "generalized_lesson": ec.generalized_lesson,
                "contest_id": contest_id,
                "interval_days": 0,
                "next_review_date": today,
            })
            added_edge_cases += 1

        if problem.specimen_candidate and problem.specimen_candidate.propose:
            last_code = problem.submissions[-1].code if problem.submissions else ""
            proposals.append({
                "id": uuid.uuid4().hex,
                "title": problem.title,
                "patterns": problem.patterns,
                "solution_code": last_code,
                "reason": problem.specimen_candidate.reason,
                "source_contest": contest_id,
                "date": contest["meta"]["date"],
            })
            added_proposals += 1

    storage.write_json("flashcards.json", flashcards)
    storage.write_json("edge_cases.json", edge_cases)
    storage.write_json("specimen_proposals.json", proposals)
    storage.write_json("elo/ratings.json", ratings)

    return {
        "contest": contest,
        "added_flashcards": added_flashcards,
        "added_edge_cases": added_edge_cases,
        "added_specimen_proposals": added_proposals,
        "updated_categories": sorted(set(updated_categories)),
    }
