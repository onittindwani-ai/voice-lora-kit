---
name: voice-lora
description: Teach a small open AI model the user's writing voice with LoRA on their own Apple Silicon Mac. Use when the user wants an AI that writes replies, emails or posts in their tone, mentions LoRA or fine tuning, or asks whether they can train a model on their computer. Runs the kit in this repo: machine check, example collection, style card, dataset build, training, and a before and after exam.
---

# Voice LoRA

Read `README.md`, `docs/00-START-HERE.md` and `docs/03-TRAIN-STEP-BY-STEP.md` before acting.

## The flow
1. `python3 tools/check_machine.py` and say the verdict in one sentence. Not an Apple Silicon Mac: read `docs/09-NOT-A-MAC.md` and be honest that it is untested.
2. Set up the environment exactly as in `docs/03`. Ask before installing.
3. Collect 50 to 100 real examples (`prompts/01-GATHER-MY-BEST-EXAMPLES.md`, `templates/examples-template.csv`). Remove private details.
4. Write the style card (`prompts/02-WRITE-MY-STYLE-CARD.md`). Only rules the person's own replies already follow.
5. `tools/build_dataset.py`, then `tools/check_data.py`. Fix every error.
6. `tools/train.py`. Report time, memory and the validation curve from `run-summary.json`.
7. `tools/compare.py` with facts, then with `--no-facts` (the honesty test). Read the answers, not only the score.

## Rules
- Everything stays on the computer. Never upload data, models or adapters.
- Stop if free disk is under 5 GB.
- LoRA teaches style, not facts. Facts go in a fact sheet in the prompt (`docs/07-LORA-OR-DOCUMENTS.md`).
- Only use flags written in `docs/03`. Otherwise read `python -m mlx_lm lora --help`.
- Never call a result good from one lucky reply. Report the numbers and the weakest answer.
