#!/usr/bin/env python3
"""Score replies against a style card: simple, mechanical, honest.

A style card is a small JSON file that says what your voice looks like in checkable terms
(greeting, sign off, length, banned words). It cannot judge warmth or taste. It can tell you
whether the reply follows your visible rules, which is what a before and after test needs.

Usage:
  python3 tools/style_check.py --card data/style-card.bluebird.json --text "Hi Priya, ..."
  python3 tools/style_check.py --card data/style-card.bluebird.json --file reply.txt
"""
import argparse
import json
import re
import sys

from common import split_reply, word_count

SENTENCE_END = re.compile(r"[.!?]+(?:\s|$)")


def count_sentences(text):
    parts = [p for p in SENTENCE_END.split(text.strip()) if p.strip()]
    return len(parts)


def check_reply(card, text):
    """Return {check_name: (passed, detail)} for one reply. Pure function."""
    greeting, body, last = split_reply(text)
    results = {}
    pattern = card.get("starts_with_regex")
    if pattern:
        ok = bool(re.search(pattern, text.strip()))
        results["greeting"] = (ok, f"starts with {text.strip()[:30]!r}")
    signoff = card.get("ends_with")
    if signoff:
        ok = text.strip().endswith(signoff)
        results["sign_off"] = (ok, f"ends with {text.strip()[-45:]!r}")
    max_words = card.get("max_words")
    if max_words:
        n = word_count(text)
        results["length"] = (n <= max_words, f"{n} words (limit {max_words})")
    max_sentences = card.get("max_sentences_in_body")
    if max_sentences:
        n = count_sentences(body)
        results["short_body"] = (n <= max_sentences, f"{n} sentences in the body (limit {max_sentences})")
    max_ex = card.get("max_exclamations")
    if max_ex is not None:
        n = text.count("!")
        results["calm"] = (n <= max_ex, f"{n} exclamation marks (limit {max_ex})")
    banned_chars = card.get("banned_characters", [])
    if banned_chars:
        hits = [c for c in banned_chars if c in text]
        results["banned_characters"] = (not hits, f"found {hits}" if hits else "none found")
    banned_phrases = card.get("banned_phrases", [])
    if banned_phrases:
        hits = [p for p in banned_phrases if p.lower() in text.lower()]
        results["banned_phrases"] = (not hits, f"found {hits}" if hits else "none found")
    return results


def says_check_first(card, text):
    """True when the reply admits it needs to check, using the card's unknown_reply_regex."""
    pattern = card.get("unknown_reply_regex")
    return bool(pattern and re.search(pattern, text))


def honesty(card, texts, kinds):
    """For questions marked unknown, a good reply admits it must check. For ordinary questions it should not.
    Returns (honest_on_unknown, unknown_total, no_false_check_on_normal, normal_total)."""
    unknown = [t for t, k in zip(texts, kinds) if k == "unknown"]
    normal = [t for t, k in zip(texts, kinds) if k != "unknown"]
    return (
        sum(1 for t in unknown if says_check_first(card, t)), len(unknown),
        sum(1 for t in normal if not says_check_first(card, t)), len(normal),
    )


def score(card, texts):
    """Return (full_pass_count, total, per_check_pass_counts)."""
    per_check, full = {}, 0
    for text in texts:
        results = check_reply(card, text)
        for name, (ok, _detail) in results.items():
            per_check[name] = per_check.get(name, 0) + (1 if ok else 0)
        if results and all(ok for ok, _ in results.values()):
            full += 1
    return full, len(texts), per_check


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--card", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text")
    group.add_argument("--file")
    args = parser.parse_args()
    card = json.load(open(args.card, encoding="utf-8"))
    text = args.text if args.text is not None else open(args.file, encoding="utf-8").read()
    results = check_reply(card, text)
    for name, (ok, detail) in results.items():
        print(f"{'PASS' if ok else 'FAIL'}  {name:18s} {detail}")
    passed = all(ok for ok, _ in results.values())
    print("All checks passed." if passed else "Some checks failed.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
