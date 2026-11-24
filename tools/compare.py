#!/usr/bin/env python3
"""The final exam: answer the held back test questions with the plain model and with your
trained model, and score both against your style card.

Needs mlx-lm (run it inside the environment where you trained).

Usage:
  python3 tools/compare.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
      --adapter-path work/adapter/best --data work/data --card data/style-card.bluebird.json
  To test a merged model instead: use --fused-model work/fused-16bit in place of --adapter-path.
  add --no-facts to ask the same questions with the fact sheet removed. Only the first line of the
  system message (the role line) is kept. This is the honesty test.
"""
import argparse
import json
import sys
from pathlib import Path

from common import read_jsonl
from style_check import honesty, score


def answer(model, tokenizer, messages, max_tokens):
    from mlx_lm import generate
    from mlx_lm.sample_utils import make_sampler

    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    return generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, sampler=make_sampler(temp=0.0)).strip()


def without_facts(messages):
    """Keep only the first line of the system message (the role line), drop the facts."""
    trimmed = []
    for m in messages:
        if m["role"] == "system":
            m = {"role": "system", "content": m["content"].splitlines()[0]}
        trimmed.append(m)
    return trimmed


def run(model_name, adapter, rows, no_facts, max_tokens):
    from mlx_lm import load

    model, tokenizer = load(model_name, adapter_path=adapter)
    outputs = []
    for row in rows:
        messages = row["messages"][:-1]
        if no_facts:
            messages = without_facts(messages)
        outputs.append(answer(model, tokenizer, messages, max_tokens))
    return outputs


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True)
    p.add_argument("--adapter-path", help="the trained adapter (use the folder called best)")
    p.add_argument("--fused-model", help="test a merged model folder instead of an adapter (see tools/fuse.py)")
    p.add_argument("--data", default="work/data")
    p.add_argument("--card", required=True)
    p.add_argument("--out", default=None, help="folder for the report (default: inside the adapter folder)")
    p.add_argument("--no-facts", action="store_true", help="remove the facts from the system message (the honesty test)")
    p.add_argument("--max-tokens", type=int, default=160)
    args = p.parse_args()

    rows = read_jsonl(Path(args.data) / "test.jsonl")
    card = json.load(open(args.card, encoding="utf-8"))
    questions = [next(m["content"] for m in r["messages"] if m["role"] == "user") for r in rows]

    if not args.adapter_path and not args.fused_model:
        p.error("give --adapter-path or --fused-model")
    print(f"Asking the plain model {len(rows)} held back questions...")
    base = run(args.model, None, rows, args.no_facts, args.max_tokens)
    print("Asking your trained model the same questions...")
    if args.fused_model:
        tuned = run(args.fused_model, None, rows, args.no_facts, args.max_tokens)
    else:
        tuned = run(args.model, args.adapter_path, rows, args.no_facts, args.max_tokens)

    base_full, total, base_by = score(card, base)
    tuned_full, _, tuned_by = score(card, tuned)
    out = Path(args.out or args.adapter_path or args.fused_model)
    out.mkdir(parents=True, exist_ok=True)
    tag = "no-facts" if args.no_facts else "with-facts"
    meta_path = Path(args.data) / "test-meta.json"
    kinds = [m["kind"] for m in json.load(open(meta_path, encoding="utf-8"))] if meta_path.exists() else ["normal"] * len(rows)
    b_ok, unknown_n, b_calm, normal_n = honesty(card, base, kinds)
    t_ok, _, t_calm, _ = honesty(card, tuned, kinds)

    lines = [f"# Before and after ({tag})", "", f"Style card: {card.get('name', args.card)}", ""]
    if args.no_facts:
        lines += ["The fact sheet was removed. Read every answer and mark where a model states something it could not know.", ""]
    lines += ["| | Plain model | Your trained model |", "| --- | --- | --- |"]
    lines.append(f"| Replies that pass every style check | {base_full} of {total} | {tuned_full} of {total} |")
    show_honesty = bool(unknown_n and card.get("unknown_reply_regex") and not args.no_facts)
    if show_honesty:
        lines.append(f"| Says it will check on questions the fact sheet cannot answer | {b_ok} of {unknown_n} | {t_ok} of {unknown_n} |")
        lines.append(f"| Does not say \"let me check\" on ordinary questions | {b_calm} of {normal_n} | {t_calm} of {normal_n} |")
    for name in sorted(set(base_by) | set(tuned_by)):
        lines.append(f"| {name} | {base_by.get(name, 0)} of {total} | {tuned_by.get(name, 0)} of {total} |")
    lines.append("")
    for question, before, after in zip(questions, base, tuned):
        lines += [f"## Question: {question}", "", "**Plain model**", "", before, "", "**Your trained model**", "", after, ""]
    (out / f"compare-{tag}.md").write_text("\n".join(lines), encoding="utf-8")
    (out / f"compare-{tag}.json").write_text(
        json.dumps({"questions": questions, "plain": base, "trained": tuned,
                    "plain_full_pass": base_full, "trained_full_pass": tuned_full, "total": total,
                    "kinds": kinds, "plain_checks_when_unknown": b_ok, "trained_checks_when_unknown": t_ok,
                    "unknown_total": unknown_n, "plain_calm_on_normal": b_calm, "trained_calm_on_normal": t_calm, "normal_total": normal_n}, indent=2),
        encoding="utf-8",
    )
    print(f"Plain model passes every style check on {base_full} of {total}. Your trained model on {tuned_full} of {total}.")
    if show_honesty:
        print(f"Says it will check when the fact sheet has no answer: plain {b_ok} of {unknown_n}, trained {t_ok} of {unknown_n}.")
    print(f"Full side by side answers: {out / f'compare-{tag}.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
