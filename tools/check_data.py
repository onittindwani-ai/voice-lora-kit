#!/usr/bin/env python3
"""Check a folder of train.jsonl, valid.jsonl and test.jsonl BEFORE you train.

Catches the mistakes that waste an evening: broken lines, wrong roles, empty replies,
the same question in training and in the final exam, and examples that are too long.

Usage: python3 tools/check_data.py work/data
"""
import sys
from pathlib import Path

from common import read_jsonl, word_count

WORDS_PER_TOKEN_GUESS = 0.75  # rough: 1 word is about 1.3 tokens
MAX_SEQ_TOKENS = 2048          # mlx-lm default for --max-seq-length


def check_rows(name, rows):
    errors, warnings = [], []
    for number, row in enumerate(rows, start=1):
        messages = row.get("messages")
        where = f"{name} line {number}"
        if not isinstance(messages, list) or len(messages) < 2:
            errors.append(f"{where}: needs a 'messages' list with at least a user and an assistant message")
            continue
        roles = [m.get("role") for m in messages]
        if roles[-1] != "assistant":
            errors.append(f"{where}: the last message must be the assistant reply, found {roles[-1]!r}")
        if "user" not in roles:
            errors.append(f"{where}: no user message")
        if any(r not in ("system", "user", "assistant") for r in roles):
            errors.append(f"{where}: unknown role in {roles}")
        for message in messages:
            if not str(message.get("content", "")).strip():
                errors.append(f"{where}: an empty {message.get('role')} message")
        total_words = sum(word_count(str(m.get("content", ""))) for m in messages)
        if total_words / WORDS_PER_TOKEN_GUESS > MAX_SEQ_TOKENS:
            warnings.append(f"{where}: about {int(total_words / WORDS_PER_TOKEN_GUESS)} tokens, longer than {MAX_SEQ_TOKENS}; it will be cut")
    return errors, warnings


def user_text(row):
    return " ".join(m.get("content", "") for m in row.get("messages", []) if m.get("role") == "user").strip().lower()


def main(folder):
    folder = Path(folder)
    errors, warnings, data = [], [], {}
    for name in ("train", "valid", "test"):
        path = folder / f"{name}.jsonl"
        if not path.exists():
            if name == "test":
                warnings.append("no test.jsonl: you will have no final exam to compare against")
            else:
                errors.append(f"missing {path}")
            continue
        try:
            data[name] = read_jsonl(path)
        except ValueError as error:
            errors.append(str(error))
            continue
        e, w = check_rows(name, data[name])
        errors += e
        warnings += w

    train_users = {user_text(r) for r in data.get("train", [])}
    for other in ("valid", "test"):
        shared = [r for r in data.get(other, []) if user_text(r) in train_users]
        if shared:
            errors.append(f"{len(shared)} {other} row(s) also appear in train: that is cheating on your own exam")

    train_n = len(data.get("train", []))
    if 0 < train_n < 20:
        errors.append(f"only {train_n} training rows; use at least 20, and 50 to 100 is a better start")
    elif 20 <= train_n < 50:
        warnings.append(f"{train_n} training rows will train, but the result may be thin")
    for name in ("valid", "test"):
        if name in data and len(data[name]) < 4:
            warnings.append(f"only {len(data[name])} {name} rows; the signal will be noisy")

    print("Counts:", ", ".join(f"{k} {len(v)}" for k, v in data.items()))
    for line in warnings:
        print("WARNING:", line)
    for line in errors:
        print("ERROR  :", line)
    if errors:
        print("Fix the errors above, then run this check again.")
        return 2
    print("Data looks ready to train.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
