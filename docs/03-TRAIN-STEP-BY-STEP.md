# Train step by step (every command here was run on a real Mac)

Tested on: MacBook with Apple M4, 16 GB memory, macOS, Python 3.12.13, `mlx-lm` 0.32.2, `mlx` 0.32.4, model
`mlx-community/Qwen2.5-1.5B-Instruct-4bit` (Apache 2.0 licence). Other setups: see `docs/01` and `docs/09`.

## 0. Check your computer

```bash
python3 tools/check_machine.py
```

It tells you if your Mac can do this and which model to start with. Keep at least 5 GB of disk free.

## 1. Make a clean environment (one time)

`mlx-lm` 0.32 needs Python 3.11 or newer. The easiest way is `uv`, a free Python tool (`brew install uv`):

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python mlx-lm
.venv/bin/python -c "import mlx_lm; print(mlx_lm.__version__)"
```

Prefer plain Python? `python3.12 -m venv .venv`, then `.venv/bin/pip install mlx-lm`. Use `.venv/bin/python` in every command
below, or run `source .venv/bin/activate` first and then plain `python`.

## 2. Build your three data files

```bash
python3 tools/build_dataset.py --csv data/sample_customer_replies.csv --system-file data/FACT-SHEET.txt --valid 8 --test 10 --out work/data
python3 tools/check_data.py work/data
```

For your own data, swap in your CSV and fact sheet (`templates/`). Fix every ERROR before going on.

## 3. Train

```bash
.venv/bin/python tools/train.py --adapter-path work/adapter
```

The first run downloads the model (839 MB) from Hugging Face, once. Defaults, from the run we measured:
60 iterations, batch size 4, 16 layers, learning rate 1e-5, a checkpoint and a validation score every 10 iterations.
On our Mac it took 6.6 minutes and peaked at 4.62 GB of memory.
When it ends, `work/adapter/run-summary.json` holds the time, peak memory, loss numbers and adapter size, and the
checkpoint with the best validation score is copied to `work/adapter/best`. **Use `best`, not the last file.**

What `train.py` runs underneath (so you can see there is no magic):

```bash
.venv/bin/python -m mlx_lm lora --model mlx-community/Qwen2.5-1.5B-Instruct-4bit --train \
  --data work/data --adapter-path work/adapter --iters 60 --batch-size 4 --num-layers 16 \
  --learning-rate 1e-5 --max-seq-length 1024 --steps-per-report 10 --steps-per-eval 10 \
  --save-every 10 --seed 7 --mask-prompt
```

`--mask-prompt` makes the model learn from the replies only, not from your fact sheet and the customer's question.
A model with 4 bit weights is trained as QLoRA automatically (Apple's `mlx-lm` documentation says so).

## 4. Take the final exam

```bash
.venv/bin/python tools/compare.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
  --adapter-path work/adapter/best --data work/data --card data/style-card.bluebird.json --out work/adapter
.venv/bin/python tools/compare.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
  --adapter-path work/adapter/best --data work/data --card data/style-card.bluebird.json --out work/adapter --no-facts
```

The second command is the honesty test: same questions, no fact sheet. See `docs/04`.

## 5. Use it

Chat with it:

```bash
.venv/bin/python -m mlx_lm chat --model mlx-community/Qwen2.5-1.5B-Instruct-4bit --adapter-path work/adapter/best
```

Or merge the add on into one standalone model folder (`docs/05`).

## If memory runs out

These come from Apple's own `mlx-lm` LoRA documentation: use a smaller `--batch-size` (the default is 4), fewer
`--num-layers` (the default we use is 16), a 4 bit model, or add `--grad-checkpoint` (slower, uses less memory).
`train.py` passes `--grad-checkpoint` through when you give it.

## Every flag we use, in plain words

| Flag | Meaning |
| --- | --- |
| `--model` | The base model to start from |
| `--data` | The folder with train, valid and test files |
| `--iters` | How many small update steps to take |
| `--batch-size` | Examples looked at per step |
| `--num-layers` | How many layers of the model get the add on |
| `--learning-rate` | How big each step is. Too big can ruin it, too small learns nothing |
| `--max-seq-length` | Longest example in tokens before cutting |
| `--steps-per-eval` | How often to take the practice quiz (validation) |
| `--save-every` | How often to save a checkpoint, so you can go back to the best one |
| `--mask-prompt` | Learn from the reply only |
