# Instructions for Claude Code and Codex in this folder

This kit helps a person teach a small open AI model their writing voice with LoRA, on their own Apple Silicon Mac.
Read `README.md`, then `docs/00-START-HERE.md`, then `docs/03-TRAIN-STEP-BY-STEP.md`.

Rules:
1. Everything stays on this computer. Never upload the person's examples, model files or adapter. Never connect to
   their email or chat accounts; they paste examples themselves.
2. Only use commands and flags written in `docs/03-TRAIN-STEP-BY-STEP.md` and the tools in `tools/`. If a flag is not
   there, run `python -m mlx_lm lora --help` first and read it. Do not guess flags.
3. Ask before installing anything, and say how much disk it uses. Stop if free disk is under 5 GB.
4. Explain each step in plain words before running it. Assume the person has never done this.
5. LoRA teaches style, not facts. When the person wants the model to know prices, hours or policies, put them in a fact
   sheet in the prompt (`docs/07-LORA-OR-DOCUMENTS.md`), never rely on training to store them.
6. Never call a result good because one reply looked good. Run `tools/compare.py` and report the numbers and the
   weakest answers honestly.
7. Do not commit `work/`, adapters, model files, the person's examples or their style card (the `.gitignore` covers them).
8. Nothing here is tested on Windows or Linux. Say so if asked. See `docs/09-NOT-A-MAC.md`.
