# Our run, saved

The files in this folder are the real output of one run of this kit, made in a fresh copy of the repository by
following `docs/03-TRAIN-STEP-BY-STEP.md` command by command, on 24 November 2026.

Machine: MacBook with Apple M4, 16 GB memory, many other apps open. `mlx-lm` 0.32.2, `mlx` 0.32.4, Python 3.12.13.
Model: `mlx-community/Qwen2.5-1.5B-Instruct-4bit`. Data: `data/sample_customer_replies.csv` (62 train, 8 valid, 10 test).

| File | What it is |
| --- | --- |
| `run-summary.json` | Time (431.6 s), peak memory (4.64 GB), validation losses, adapter size (20.15 MB) |
| `training.log` | The training log with colour codes removed |
| `compare-with-facts.md` | The exam with the fact sheet: score table and every answer, plain model against trained |
| `compare-no-facts.md` | The honesty test: facts removed, same questions |

Your numbers will differ. See `docs/08-HONEST-LIMITS.md`.
