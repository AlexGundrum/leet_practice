from typing import Any, Literal, Optional

from pydantic import BaseModel


class Attempt(BaseModel):
    id: str
    algorithm_id: str
    title: str
    timestamp: int
    time_taken_ms: int
    passed: bool
    mode: str


class PersonalBest(BaseModel):
    best_time_ms: int
    attempt_count: int
    first_passed_at: int


class TestCase(BaseModel):
    call: str
    expected: str


class CustomAlgorithm(BaseModel):
    id: str
    title: str
    stub: str
    test_cases: list[TestCase]
    tags: list[str] = []
    difficulty: str
    # Optional fields present on full algorithms.json entries but not required for
    # user-authored custom algorithms.
    inputs_given: Optional[str] = None
    description: Optional[str] = None
    solution_code: Optional[str] = None
    solution_explanation: Optional[str] = None
    when_to_use: Optional[str] = None


class Playlist(BaseModel):
    id: str
    name: str
    isDynamic: bool = False
    algorithms: list[str] = []


class LegacyImportPayload(BaseModel):
    attempts: list[dict[str, Any]] = []
    personal_bests: dict[str, Any] = {}
    custom_algorithms: list[dict[str, Any]] = []
    playlists: list[dict[str, Any]] = []


# --- Contest capture (same-day) ---

class ContestMeta(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    type: Literal["official", "virtual"]


class SubmissionCapture(BaseModel):
    code: str
    verdict: str
    failing_test: Optional[str] = None
    notes: Optional[str] = None


class ProblemCapture(BaseModel):
    title: str
    link: Optional[str] = None
    patterns: list[str] = []
    submissions: list[SubmissionCapture] = []
    narrative: Optional[str] = None
    time_to_solve_min: Optional[float] = None


class Contest(BaseModel):
    id: str
    meta: ContestMeta
    problems: list[ProblemCapture] = []
    grading_result: Optional[dict[str, Any]] = None
    grading_imported_at: Optional[int] = None


# --- Grading import (pasted AI JSON, next-day reflection) ---

class GradingSubmission(BaseModel):
    code: str = ""
    verdict: str = ""
    failing_test: str = ""
    ai_note: str = ""


class GradingCritique(BaseModel):
    thinking_process_score: int
    what_went_right: str = ""
    what_went_wrong: str = ""
    root_cause_of_delay: str = ""


class GeneratedFlashcard(BaseModel):
    front: str
    back: str
    tag: str = ""


class EdgeCaseMissed(BaseModel):
    category: str
    description: str = ""
    generalized_lesson: str = ""


class SpecimenCandidate(BaseModel):
    propose: bool = False
    reason: str = ""


class GradingProblem(BaseModel):
    title: str
    patterns: list[str] = []
    verdict: str
    difficulty: str = "medium"
    submissions: list[GradingSubmission] = []
    critique: GradingCritique
    flashcards_generated: list[GeneratedFlashcard] = []
    edge_cases_missed: list[EdgeCaseMissed] = []
    specimen_candidate: Optional[SpecimenCandidate] = None


class GradingContestMeta(BaseModel):
    name: str = ""
    date: str = ""
    type: str = ""
    problems_attempted: int = 0
    problems_solved: int = 0


class OverallSummary(BaseModel):
    strengths: str = ""
    weaknesses: str = ""
    recommended_focus_next_week: str = ""


class GradingImport(BaseModel):
    contest_meta: GradingContestMeta
    per_problem: list[GradingProblem]
    overall_summary: OverallSummary


# --- Specimen library (curated, approval-gated) ---

class SpecimenProblem(BaseModel):
    id: str
    title: str
    tags: list[str] = []
    difficulty: str = "medium"
    stub: Optional[str] = None
    test_cases: list[TestCase] = []
    description: Optional[str] = None
    solution_code: Optional[str] = None
    solution_explanation: Optional[str] = None
    when_to_use: Optional[str] = None
    source_contest: str
    pattern_tag: str
    date: str


class SpecimenProposal(BaseModel):
    id: str
    title: str
    patterns: list[str] = []
    solution_code: str = ""
    reason: str = ""
    source_contest: str
    date: str
