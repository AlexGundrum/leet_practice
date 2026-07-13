"""Standalone contest-pacing reminder.

Run via Windows Task Scheduler, independent of whether the AlgoRep server is
running - it reads data/contests/*.json directly and sends a Gmail SMTP email
only if this week's contest count is behind the day-of-week threshold in
api/pacing.py.

Setup (one-time, done by you - this script never receives your credentials
from anywhere but your own local config file):
  1. Generate a Gmail App Password: https://myaccount.google.com/apppasswords
     (requires 2-Step Verification enabled on the Google account).
  2. Copy config/reminder.local.json.example to config/reminder.local.json
     and fill in gmail_address / app_password / to_address. That file is
     gitignored - it must never be committed.
  3. Test it manually first:
       python scripts/pacing_reminder.py
  4. Register the scheduled task (run once, from a normal command prompt):
       schtasks /create /tn "AlgoRep Pacing Reminder" /tr "\"<path-to-python.exe>\" \"<path-to-this-script>\"" /sc daily /st 18:00
     Replace both bracketed paths with absolute paths on your machine, e.g.:
       schtasks /create /tn "AlgoRep Pacing Reminder" /tr "\"C:\\Python310\\python.exe\" \"C:\\Users\\alexg\\code\\leet_practice\\scripts\\pacing_reminder.py\"" /sc daily /st 18:00
"""

import json
import smtplib
import ssl
import sys
from datetime import date
from email.mime.text import MIMEText
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from api import pacing, storage  # noqa: E402

CONFIG_PATH = REPO_ROOT / "config" / "reminder.local.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise SystemExit(
            f"Missing {CONFIG_PATH}.\n"
            "Copy config/reminder.local.json.example to config/reminder.local.json "
            "and fill in your Gmail address, App Password, and recipient address first."
        )
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def send_reminder_email(config: dict, status: dict) -> None:
    body = (
        f"You're at {status['logged']}/{status['expected']} contests logged this week "
        f"(week of {status['week_start']}). Log one today to stay on pace for 3/week."
    )
    msg = MIMEText(body)
    msg["Subject"] = "AlgoRep: contest pacing reminder"
    msg["From"] = config["gmail_address"]
    msg["To"] = config["to_address"]

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(config["gmail_address"], config["app_password"])
        server.send_message(msg)


def main() -> None:
    contest_dates = storage.load_contest_dates()
    status = pacing.pacing_status(contest_dates, date.today())

    if not status["behind"]:
        print(f"On pace: {status['logged']}/{status['expected']} this week. No email sent.")
        return

    config = load_config()
    send_reminder_email(config, status)
    print(
        f"Behind pace ({status['logged']}/{status['expected']} this week) - "
        f"reminder email sent to {config['to_address']}."
    )


if __name__ == "__main__":
    main()
