import json
import os
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _path(relative_path: str) -> Path:
    return DATA_DIR / relative_path


def read_json(relative_path: str, default: Any):
    path = _path(relative_path)
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(relative_path: str, value: Any) -> None:
    path = _path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(value, f, indent=2)
    os.replace(tmp_path, path)


def append_jsonl(relative_path: str, record: Any) -> None:
    path = _path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def read_jsonl(relative_path: str) -> list:
    path = _path(relative_path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def list_contest_files() -> list[Path]:
    contests_dir = _path("contests")
    if not contests_dir.exists():
        return []
    return sorted(contests_dir.glob("*.json"))


def load_contest_dates() -> list[str]:
    dates = []
    for path in list_contest_files():
        contest = read_json(f"contests/{path.name}", None)
        if contest:
            dates.append(contest["meta"]["date"])
    return dates
