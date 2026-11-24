---
description: Train a small LoRA with the kit's tested settings
---
Follow `docs/03-TRAIN-STEP-BY-STEP.md`. First run `python3 tools/check_data.py work/data` and stop on any error.
Then run `python3 tools/train.py` with the defaults and report the contents of `work/adapter/run-summary.json`
in plain words: minutes, peak memory, adapter size, and whether the validation loss went down and then up.
