# Changelog

## 1.0.0

First release.

- Tools: machine check, dataset builder with a private data scan and a seeded split, data checker, trainer that keeps the
  best checkpoint and records time and memory, style checker, before and after exam with an honesty score, safe merge.
- 80 sample replies from a made up bakery, with a fact sheet and a style card. 23 are "I will check" answers.
- 11 numbered guides, a glossary, a sources file, 5 prompts, 3 templates, a Claude Code skill and 3 commands.
- 29 standard library tests and a GitHub Actions workflow that runs them.
- Measured on a MacBook with Apple M4 and 16 GB, `mlx-lm` 0.32.2, Qwen2.5 1.5B Instruct 4 bit: 60 iterations in 7.2 minutes,
  peak memory 4.64 GB, adapter 20.15 MB, style checks 0 of 10 before and 10 of 10 after. Saved in `examples/our-run/`.
- Known gaps: one machine, one model, ten exam questions, nothing tested off a Mac. See `docs/08-HONEST-LIMITS.md`.
