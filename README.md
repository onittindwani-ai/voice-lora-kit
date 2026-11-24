# Voice LoRA Kit

Teach a free AI model to write the way **you** write, on your own Apple Silicon Mac, with a test that tells you
if it worked and a list of the ways people ruin it.

LoRA (said "LOH-rah", short for Low-Rank Adaptation) is a way to train a small add on file that sits on top of an AI model
and changes how it writes, without retraining the whole model. This kit gives you the examples, the tools, the exam
and the honest limits. It was built and tested on a real MacBook. Every number below is from that run.

## The idea in one picture

An AI model is a brilliant new hire who read the whole internet and writes to your customers like a Wikipedia article
having a panic attack. You do not send them back to university for 4 years. You give them a **practice week** with 60 of
your best real replies. What they learn fits in a thin binder (about 20 MB) you can slip in or out. Their degree stays untouched.
The practice week teaches **how you talk**. It does not teach **what is true**: prices and hours go on a fact sheet.
Read `docs/00-START-HERE.md`.

## What happened in our run

| | Plain model | After 7 minutes of training |
| --- | --- | --- |
| Replies that follow the style card (10 held back questions) | 0 of 10 | **10 of 10** |
| Says "let me check" when the fact sheet has no answer | 0 of 3 | **3 of 3** |
| Answers stating something unsupported or wrong (hand read) | 5 of 10 | 0 of 10 |
| With the fact sheet removed, answers stating things it could not know | 7 of 10 | 3 of 10 |

Training took 7.2 minutes and peaked at 4.64 GB of memory on an M4 MacBook with 16 GB. It also got something wrong:
it said "let me check" on 3 of 7 ordinary questions, and without the fact sheet it still invented answers.
`docs/04-TEST-LIKE-A-GRADER.md` shows the real answers, good and bad. The saved output is in `examples/our-run/`.

## What is in the box

| Folder | What it holds |
| --- | --- |
| `docs/` | 11 numbered guides (00 to 10) plus a glossary and a facts and sources file. Start with `00-START-HERE.md` |
| `docs/06-WHERE-PEOPLE-GO-WRONG.md` | **10 mistakes**, each with symptom, evidence and fix |
| `tools/` | 7 tools: machine check, dataset builder, data checker, trainer, style checker, before and after exam, safe merge |
| `data/` | **80 sample replies** from a made up bakery (23 of them "I will check" answers), its fact sheet and its style card |
| `prompts/` | 5 paste in prompts for Claude Code or Codex |
| `templates/` | Your own examples sheet, style card and fact sheet to fill in |
| `tests/` | 29 tests that run on any computer, standard library only |
| `.claude/` | A Claude Code skill and 3 slash commands that run the whole job |
| `examples/our-run/` | The real output of one run: log, summary, before and after |

## Quick start

**Easiest:** open Claude Code or Codex in this folder and paste `prompts/00-QUICK-START-FOR-CLAUDE-CODE.md`. It explains each
step in plain words and asks before it installs anything.

**By hand:** follow `docs/03-TRAIN-STEP-BY-STEP.md`. In short:

```bash
python3 tools/check_machine.py
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python mlx-lm
python3 tools/build_dataset.py --csv data/sample_customer_replies.csv --system-file data/FACT-SHEET.txt --valid 8 --test 10 --out work/data
python3 tools/check_data.py work/data
.venv/bin/python tools/train.py --adapter-path work/adapter
.venv/bin/python tools/compare.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit --adapter-path work/adapter/best --card data/style-card.bluebird.json --out work/adapter
```

Then swap in your own examples: `templates/examples-template.csv` and `docs/02-COLLECT-YOUR-EXAMPLES.md`.

## What you need

- A Mac with Apple Silicon (M1 or newer). 16 GB of memory is what we tested. 5 GB of free disk.
- Python 3.11 or newer for the training tools. The data tools run on Python 3.10 or newer (tested on 3.10 and 3.14).
- Not on a Mac? Read `docs/09-NOT-A-MAC.md`. We have not tested anything there.

## Honest limits

LoRA teaches style, not facts. A small model stays small. One Mac, one afternoon and ten exam questions are one
data point. Merging into the compressed model **loses the voice** unless you merge with `--dequantize`, which `tools/fuse.py` does for you.
Always have a person read anything that matters before it goes out. Everything stays on your computer, and the sample
bakery, its owner and its facts are made up. Full list: `docs/08-HONEST-LIMITS.md`.

## Licence

MIT, see `LICENSE`. The base model used here, Qwen2.5 1.5B Instruct, is Apache 2.0. Its 4 bit version comes from `mlx-community`.
Sources and what we verified: `docs/FACTS-AND-SOURCES.md`.
