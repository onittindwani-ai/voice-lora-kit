# Troubleshooting

| What you see | What it means | What to do |
| --- | --- | --- |
| `check_machine.py` says "cannot run the MLX path" | Not an Apple Silicon Mac | `docs/09-NOT-A-MAC.md` |
| `mlx-lm` will not install, or "requires Python" | Your Python is older than 3.11 | Make the environment with `uv venv --python 3.12 .venv` (`docs/03`) |
| "unauthenticated requests to the HF Hub" warning | Hugging Face is telling you that a login gives faster downloads | Harmless for a public model. Ignore it |
| The first run sits on "Fetching files" | It is downloading the model once (839 MB). On our run that took 4 min 35 s | Wait. The second run starts straight away |
| `build_dataset.py` says "Stop: possible private data" | It found an email, phone number, card style number or link | Remove or replace it, or use `--allow-private` only if you are sure |
| `check_data.py` says "also appear in train" | The same question is in two files | Rebuild with `build_dataset.py`. Never move rows by hand |
| `check_data.py` says "last message must be the assistant" | Your JSONL lines are in the wrong order | Rebuild from the CSV |
| Out of memory, or the Mac freezes | The job is bigger than your free memory | Close other apps. Then lower `--batch-size`, lower `--num-layers`, try `--grad-checkpoint`, or use the 0.5B model (Apple's `mlx-lm` LoRA guide lists the same options) |
| Training is much slower than the numbers in `docs/03` | Many apps open, memory pressure, a different Mac | Close apps. Our run was slowed by a busy Mac. Time is not a quality problem |
| Validation loss goes up while training loss goes down | Overfitting, the model is memorising | Use `work/adapter/best` and train fewer iterations (`docs/06`, mistake 4) |
| Every reply sounds the same, or repeats your examples | Too many iterations, or too few and too similar examples | Same as above, then add more varied examples |
| The trained model invents prices or hours | It learned the voice, not the facts | Put a fact sheet in the prompt (`docs/07`) |
| "adapter" errors when loading | The adapter was trained on a different model | Always use the same `--model` for training and for running |
| `compare.py` shows 0 of 6 for both | Your style card may not match your own examples | Run `tools/style_check.py` on three of your own replies (`prompts/02`) |
| Not sure if it worked | One good reply proves nothing | Run `compare.py` and read the weakest answers |
