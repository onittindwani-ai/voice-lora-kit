#!/usr/bin/env python3
"""Turn a spreadsheet (CSV) of your best real examples into the three files LoRA training needs.

Input : a CSV with one column for what the customer wrote and one for the reply you want copied.
Output: train.jsonl, valid.jsonl, test.jsonl in the chat format that mlx-lm reads.

Usage:
  python3 tools/build_dataset.py --csv data/sample_customer_replies.csv \
      --system-file data/FACT-SHEET.txt --out work/data
"""
import argparse
import csv
import json
import random
import re
import sys
from pathlib import Path

from common import write_jsonl

MIN_ROWS_ERROR = 20
MIN_ROWS_WARN = 50
PRIVATE_PATTERNS = {
    "an email address": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "a phone number": re.compile(r"(?<!\d)(?:\+?\d[\s().-]?){9,14}\d(?!\d)"),
    "a card style number": re.compile(r"(?<!\d)(?:\d[ -]?){13,16}(?!\d)"),
    "a web link": re.compile(r"https?://\S+"),
}


def read_rows(path, message_col, reply_col, kind_col="kind"):
    """Return (message, reply, kind) rows. The kind column is optional: mark rows whose answer is
    NOT in your fact sheet with the word unknown, so the exam can check the model does not guess."""
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in (message_col, reply_col) if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(
                f"The CSV has columns {reader.fieldnames}. Missing: {missing}. "
                "Use --message-col and --reply-col to name your columns."
            )
        has_kind = kind_col in (reader.fieldnames or [])
        return [
            (row[message_col].strip(), row[reply_col].strip(), (row[kind_col].strip().lower() or "normal") if has_kind else "normal")
            for row in reader
            if row[message_col].strip() and row[reply_col].strip()
        ]


def drop_duplicates(rows):
    seen, kept, dropped = set(), [], 0
    for row in rows:
        key = re.sub(r"\s+", " ", row[0].lower())
        if key in seen:
            dropped += 1
            continue
        seen.add(key)
        kept.append(row)
    return kept, dropped


def find_private(rows):
    found = []
    for index, (message, reply, _kind) in enumerate(rows, start=2):  # row 1 is the header
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(message) or pattern.search(reply):
                found.append((index, label))
    return found


def to_example(system, message, reply):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})
    messages.append({"role": "assistant", "content": reply})
    return {"messages": messages}


def split_counts(total, valid, test):
    test = test if test is not None else max(4, round(total * 0.08))
    valid = valid if valid is not None else max(4, round(total * 0.08))
    return valid, test


def stratified_split(rows, test_n, valid_n, seed):
    """Shuffle, then make sure the final exam holds some unknown rows (questions the fact sheet cannot
    answer), in proportion to how common they are, so the exam can test honesty."""
    shuffled = rows[:]
    random.Random(seed).shuffle(shuffled)
    unknown = [r for r in shuffled if r[2] == "unknown"]
    normal = [r for r in shuffled if r[2] != "unknown"]
    take_unknown = 0
    if len(unknown) >= 9:
        take_unknown = min(len(unknown), max(3, round(test_n * len(unknown) / len(shuffled))))
    test_rows = unknown[:take_unknown] + normal[: test_n - take_unknown]
    rest = unknown[take_unknown:] + normal[test_n - take_unknown :]
    random.Random(seed + 1).shuffle(rest)
    return test_rows, rest[:valid_n], rest[valid_n:]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", default="work/data")
    parser.add_argument("--message-col", default="customer_message")
    parser.add_argument("--reply-col", default="reply")
    parser.add_argument("--kind-col", default="kind", help="optional column: write unknown on rows the fact sheet cannot answer")
    parser.add_argument("--system-file", help="text file with facts and rules, put in every example")
    parser.add_argument("--valid", type=int, help="rows held out to watch training (default about 8 percent)")
    parser.add_argument("--test", type=int, help="rows kept back for the final exam (default about 8 percent)")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--allow-private", action="store_true", help="skip the private data stop (not recommended)")
    args = parser.parse_args()

    rows = read_rows(args.csv, args.message_col, args.reply_col, args.kind_col)
    rows, dropped = drop_duplicates(rows)
    if dropped:
        print(f"Removed {dropped} duplicate message(s).")
    if len(rows) < MIN_ROWS_ERROR:
        print(f"Only {len(rows)} usable rows. You need at least {MIN_ROWS_ERROR}, and 50 to 100 is a better start.")
        return 2
    if len(rows) < MIN_ROWS_WARN:
        print(f"Warning: {len(rows)} rows will train, but the result may be thin. Aim for 50 to 100.")

    private = find_private(rows)
    if private and not args.allow_private:
        print("Stop: possible private data found. Remove or replace it, then run again.")
        for row, label in private[:20]:
            print(f"  CSV row {row}: {label}")
        print("Use --allow-private only if you are sure these are safe to train on.")
        return 2

    system = Path(args.system_file).read_text(encoding="utf-8").strip() if args.system_file else ""
    valid_n, test_n = split_counts(len(rows), args.valid, args.test)
    if valid_n + test_n >= len(rows) - 10:
        print("Too few rows for the requested validation and test sizes.")
        return 2

    test_rows, valid_rows, train_rows = stratified_split(rows, test_n, valid_n, args.seed)

    out = Path(args.out)
    write_jsonl(out / "train.jsonl", [to_example(system, m, r) for m, r, _ in train_rows])
    write_jsonl(out / "valid.jsonl", [to_example(system, m, r) for m, r, _ in valid_rows])
    write_jsonl(out / "test.jsonl", [to_example(system, m, r) for m, r, _ in test_rows])
    (out / "test-meta.json").write_text(json.dumps([{"kind": k} for _, _, k in test_rows], indent=2), encoding="utf-8")
    summary = {
        "unknown_rows_in_test": sum(1 for _, _, k in test_rows if k == "unknown"),
        "source": str(args.csv),
        "rows_used": len(rows),
        "train": len(train_rows),
        "valid": len(valid_rows),
        "test": len(test_rows),
        "seed": args.seed,
        "system_message": bool(system),
    }
    (out / "split-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {out}/train.jsonl ({len(train_rows)}), valid.jsonl ({len(valid_rows)}), test.jsonl ({len(test_rows)}).")
    print("The test file is your final exam. Training never sees it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
