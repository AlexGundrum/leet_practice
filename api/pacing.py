"""Weekly contest-pacing logic, shared by the live API endpoint and the
standalone reminder script (so both agree on what "behind pace" means).
"""

from datetime import date, timedelta
from typing import Optional

# Day-of-week -> minimum contests that should be logged so far this week.
# Tunable by hand to match the actual LeetCode weekly/biweekly calendar -
# no calendar-API integration, attendance is logged manually.
THRESHOLDS = {
    "Mon": 0,
    "Tue": 0,
    "Wed": 1,
    "Thu": 1,
    "Fri": 2,
    "Sat": 2,
    "Sun": 3,
}


def week_start_for(today: date) -> date:
    return today - timedelta(days=today.weekday())


def week_progress(contest_dates: list[str], today: date) -> int:
    start = week_start_for(today)
    count = 0
    for d in contest_dates:
        contest_date = date.fromisoformat(d)
        if start <= contest_date <= today:
            count += 1
    return count


def pacing_status(contest_dates: list[str], today: Optional[date] = None) -> dict:
    today = today or date.today()
    logged = week_progress(contest_dates, today)
    expected = THRESHOLDS[today.strftime("%a")]
    return {
        "logged": logged,
        "expected": expected,
        "behind": logged < expected,
        "week_start": week_start_for(today).isoformat(),
    }
