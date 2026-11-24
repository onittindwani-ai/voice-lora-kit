"""Small shared helpers for the kit tools. Standard library only."""
import json
import shutil
from pathlib import Path


def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"{path} line {number} is not valid JSON: {error}") from error
    return rows


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def free_disk_gb(path="."):
    return shutil.disk_usage(path).free / 1024**3


def word_count(text):
    return len(text.split())


def split_reply(text):
    """Return (greeting_line, body, last_line) of a reply written as greeting, body, sign-off."""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if len(lines) < 3:
        return (lines[0] if lines else "", " ".join(lines[1:]), "")
    return lines[0], " ".join(lines[1:-1]), lines[-1]
