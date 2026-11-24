# Can my computer do this?

Run `python3 tools/check_machine.py`. This page explains what it checks and what we measured.

## The one hard requirement

An **Apple Silicon Mac** (M1 or newer). The training tool, Apple's MLX, does not run on Windows, Linux or Intel Macs.
Not on a Mac? `docs/09-NOT-A-MAC.md` has pointers. We have not tested them.

## What we measured (one machine, one run, so read it as an example)

| Item | Measured |
| --- | --- |
| Computer | MacBook, Apple M4, 16 GB memory, many other apps open at the time |
| Model | `mlx-community/Qwen2.5-1.5B-Instruct-4bit` (839 MB on disk) |
| Examples | 58 for training, 6 to watch, 6 for the final exam |
| Settings | 60 iterations, batch size 4, 16 layers, learning rate 1e-5 |
| **Training time** | **393 seconds (6.6 minutes)**, about 6 seconds per iteration on a busy Mac |
| **Peak memory** | **4.62 GB** (measured by the operating system, `/usr/bin/time -l`) |
| **Adapter size** | **20.15 MB** per saved checkpoint |
| First download of the model | 4 min 35 s on our connection, once |
| Disk used by tools | about 367 MB for the Python environment, 839 MB for the model |
| Trainable numbers | 5.276M of 1,543.714M (0.342 percent) |

The first, longer run (150 iterations) took 20.7 minutes in total, including the 4 min 35 s download.

## What to expect on other Macs (rule of thumb, NOT measured by us)

| Memory | Suggested start |
| --- | --- |
| 16 GB or more | The 1.5B model above (tested) |
| 8 to 15 GB | The 0.5B model first (`mlx-community/Qwen2.5-0.5B-Instruct-4bit`). Untested by us |
| Under 8 GB | Tight. Try the 0.5B model with `--batch-size 1` and `--grad-checkpoint`. Untested by us |
| 32 GB or more | You may try bigger models. Untested by us. Check each model's licence |

Apple's own LoRA guide shows a 7B model on a 32 GB Mac. We did not run it and make no promise about it.

## Free disk

Keep at least 5 GB free. Each saved checkpoint is about 20 MB, and a default run keeps 6 of them plus the final and best copies, so about 160 MB.

## Make it faster, or lighter

Close big apps before you start. A busy Mac swaps memory to disk and slows training. If memory is the problem, the
options from Apple's `mlx-lm` guide are a smaller `--batch-size`, fewer `--num-layers`, a 4 bit model (already the
default here), or `--grad-checkpoint`.
