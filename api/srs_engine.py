"""Spaced-repetition scheduling.

Flashcards use the textbook SM-2 algorithm (4-button grading collapsed onto the
original 0-5 quality scale). Edge cases use a deliberately simpler binary
remembered/missed doubling scheme, since they're framed as quick-recall quizzes,
not deep-retention flashcards.
"""

import random
import time
from datetime import date, timedelta

QUALITY_BY_GRADE = {"again": 0, "hard": 3, "good": 4, "easy": 5}

# Once a card's scheduled interval reaches this many days, treat it as
# "mastered" - it's still due, but shown less often the further out it's
# scheduled, so review sessions stay weighted toward what's actually shaky
# instead of re-showing things you've clearly already got.
DEFAULT_MASTERY_THRESHOLD_DAYS = 21
MASTERY_MIN_PROBABILITY = 0.15


def review_flashcard(card: dict, grade: str) -> dict:
    q = QUALITY_BY_GRADE[grade]

    ease_factor = card.get("ease_factor", 2.5)
    interval_days = card.get("interval_days", 0)
    repetitions = card.get("repetitions", 0)

    if q < 3:
        repetitions = 0
        interval_days = 1
    else:
        if repetitions == 0:
            interval_days = 1
        elif repetitions == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
        repetitions += 1

    ease_factor = max(1.3, ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))

    return {
        **card,
        "ease_factor": ease_factor,
        "interval_days": interval_days,
        "repetitions": repetitions,
        "next_review_date": (date.today() + timedelta(days=interval_days)).isoformat(),
        "last_reviewed_at": int(time.time() * 1000),
    }


def review_edge_case(edge_case: dict, remembered: bool) -> dict:
    if remembered:
        interval_days = min((edge_case.get("interval_days") or 1) * 2, 30)
    else:
        interval_days = 1

    return {
        **edge_case,
        "interval_days": interval_days,
        "next_review_date": (date.today() + timedelta(days=interval_days)).isoformat(),
    }


def inclusion_probability(interval_days: int, mastery_threshold: int = DEFAULT_MASTERY_THRESHOLD_DAYS) -> float:
    if interval_days < mastery_threshold:
        return 1.0
    return max(MASTERY_MIN_PROBABILITY, mastery_threshold / interval_days)


def should_include_due_card(interval_days: int, mastery_threshold: int = DEFAULT_MASTERY_THRESHOLD_DAYS) -> bool:
    """Cards below the mastery threshold always show when due. Past it, inclusion
    probability decays smoothly (floored so nothing fully disappears forever) -
    the more over-mastered a card is, the rarer it becomes in a review session."""
    return random.random() < inclusion_probability(interval_days, mastery_threshold)
