# Facts and sources

Checked on 24 November 2026. Labels: **P** primary source read directly, **M** measured by us in this kit,
**I** inference or practitioner advice (not measured), **U** unverified.

## About LoRA and QLoRA

| Claim | Label | Source and what it says |
| --- | --- | --- |
| LoRA freezes the pretrained weights and adds small trainable low rank matrices to each layer | P | Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", arXiv 2106.09685, abstract |
| For GPT-3 175B it can cut trainable parameters by 10,000 times and GPU memory by 3 times, with no extra delay when running | P | Same abstract. These figures are for that huge model, not for the 1.5B model used here |
| QLoRA fine tunes a frozen 4 bit quantized model with adapters | P | Dettmers et al., "QLoRA: Efficient Finetuning of Quantized LLMs", arXiv 2305.14314, abstract |
| QLoRA on a small, high quality dataset can give state of the art results | P | Same abstract (it says this about its own benchmarks, not about every task) |
| In `mlx-lm`, pointing `--model` at a quantized model trains with QLoRA | P | Apple `mlx-lm` LoRA guide (`mlx_lm/LORA.md`) |
| Memory options: smaller `--batch-size`, fewer `--num-layers`, a quantized model, `--grad-checkpoint` | P | Same guide, section on memory use |
| Apple's guide reports about 250 tokens per second for a 7B model on an M1 Max with 32 GB | P | Same guide. We did not reproduce it |
| `mlx-lm` is MIT licensed, version 0.32.2 needs Python 3.11 or newer | P | GitHub repository `ml-explore/mlx-lm` and PyPI, read 24 Nov 2026 |
| Qwen2.5 1.5B Instruct is Apache 2.0, and so is the `mlx-community` 4 bit conversion used here | P | Hugging Face model cards for `Qwen/Qwen2.5-1.5B-Instruct` and `mlx-community/Qwen2.5-1.5B-Instruct-4bit` |
| The 3B Qwen2.5 model uses a different licence ("other") | P | Hugging Face card for `mlx-community/Qwen2.5-3B-Instruct-4bit`. Read it before commercial use |
| Hugging Face PEFT, Unsloth and Axolotl are Apache 2.0 projects | P | GitHub repository pages, read 24 Nov 2026. We did not run them |
| OpenAI offers a fine tuning guide for its hosted models | P | `platform.openai.com/docs/guides/fine-tuning` loads (HTTP 200). We did not read its details |

## What we measured (one MacBook, Apple M4, 16 GB, many apps open)

All numbers in `docs/01`, `docs/03`, `docs/04` and `docs/06` come from `work/adapter/run-summary.json`,
the exam reports and the training log of the runs described there. The final numbers are in the
`CHANGELOG.md` entry for v1.0.0 so they are easy to find.

| Claim | Label |
| --- | --- |
| Training and exam numbers for the 1.5B 4 bit model on this sample | M, one run each, one machine |
| Validation loss is best near iteration 30 and rises after it, in two different runs | M |
| Merging into the 4 bit model loses the voice, merging with `--dequantize` keeps it | M, once. The cause (rounding when squeezed back to 4 bit) is **I**, not proved |
| Answers with and without the fact sheet, hand read | M, one reader, ten questions: not a benchmark |

## Advice we did not measure

| Claim | Label |
| --- | --- |
| 50 to 100 clean examples is a sensible first target | I (practitioner advice, in line with the QLoRA paper's point about small high quality data) |
| Messy or inconsistent examples teach messy or inconsistent behaviour | I |
| Try a better prompt and a fact sheet before training | I |
| Other Macs, other model sizes, Windows, Linux | U, untested |
| Sample data and the fact sheet | The bakery, its owner and all its facts are made up for this kit |
