"""Per-category Elo-style rating updates.

Blends an objective performance signal (solved/unsolved, submission count, time
relative to a difficulty-based expectation) with an AI-assessed signal (how much
the critique's root-cause-of-delay implicates this specific category), then applies
a standard Elo expected-vs-actual update against a difficulty-based opponent rating.
"""

DIFFICULTY_OPPONENT_RATING = {"easy": 1000, "medium": 1300, "hard": 1600}
EXPECTED_TIME_MIN = {"easy": 10, "medium": 20, "hard": 35}
DEFAULT_RATING = 1200

# thinking_process_score 1 (worst) -> 5 (best), mapped to severity 1.0 -> 0.0
SEVERITY_BY_SCORE = {1: 1.0, 2: 0.75, 3: 0.5, 4: 0.25, 5: 0.0}


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def is_implicated(category: str, root_cause_text: str) -> bool:
    """Simple keyword match, not NLP - checks if the category name (or its
    underscore/hyphen-normalized form) appears in the critique's free text."""
    if not root_cause_text or not category:
        return False
    normalized_category = category.lower().replace("_", " ").replace("-", " ").strip()
    normalized_text = root_cause_text.lower().replace("_", " ").replace("-", " ")
    return normalized_category in normalized_text


def objective_score(solved: bool, submission_count: int, time_to_solve_min: float | None, difficulty: str) -> float:
    expected = EXPECTED_TIME_MIN.get(difficulty, 20)
    if time_to_solve_min is None:
        time_factor = 0.0
    else:
        time_factor = clamp(1 - (time_to_solve_min / expected), -1, 1)

    score = (
        0.5
        + 0.3 * (1 if solved else -1)
        + 0.2 * time_factor
        - 0.1 * max(0, submission_count - 1)
    )
    return clamp(score, 0, 1)


def ai_adjustment(implicated: bool, thinking_process_score: int) -> float:
    severity = SEVERITY_BY_SCORE.get(thinking_process_score, 0.5)
    return -0.5 * (1 if implicated else 0) * severity


def blended_actual_score(s_obj: float, s_ai: float) -> float:
    return clamp(0.7 * s_obj + 0.3 * (0.5 + 0.5 * s_ai), 0, 1)


def expected_score(category_rating: float, opponent_rating: float) -> float:
    return 1 / (1 + 10 ** ((opponent_rating - category_rating) / 400))


def k_factor(n_updates: int) -> float:
    if n_updates < 10:
        return 40
    if n_updates < 30:
        return 24
    return 16


def update_category_rating(current_state: dict, s_obj: float, s_ai: float, difficulty: str) -> tuple[dict, dict]:
    """Returns (new_state_for_ratings_json, history_row_extra_fields)."""
    rating = current_state.get("rating", DEFAULT_RATING)
    n_updates = current_state.get("n_updates", 0)
    opponent = DIFFICULTY_OPPONENT_RATING.get(difficulty, 1300)

    s_actual = blended_actual_score(s_obj, s_ai)
    e = expected_score(rating, opponent)
    k = k_factor(n_updates)
    new_rating = rating + k * (s_actual - e)

    new_state = {
        "rating": new_rating,
        "k": k,
        "n_updates": n_updates + 1,
    }
    history_extra = {
        "old_rating": rating,
        "new_rating": new_rating,
        "s_obj": s_obj,
        "s_ai": s_ai,
        "s_actual": s_actual,
        "e": e,
        "k": k,
    }
    return new_state, history_extra
