# Honest limits

What this kit does not do, what we did not test, and what you should not promise anyone.

## What was tested, and what was not

| Claim | Status |
| --- | --- |
| The kit's tools run and the standard library tests pass | Tested (`python -m unittest discover -s tests`) |
| A 1.5B 4 bit model trains a LoRA on 58 examples on a 16 GB Apple M4 | **Tested once**, on one Mac |
| Before and after, scored against a mechanical style card | Tested once, six held out questions. See `docs/04` |
| Other Macs, other model sizes (0.5B, 3B, 7B) | **Not tested.** The 0.5B model is offered as the lighter first try. Treat larger sizes as your own experiment |
| Windows, Linux, Intel Macs | **Not tested**, MLX cannot run there. See `docs/09` |
| Your own data | Not tested, it is yours. The tools check the format, not whether your examples are good |
| Fusing and exporting | Tested on one run. See `docs/05` |

## What LoRA cannot do

- **It does not teach facts.** It copies a style. Facts go in a fact sheet (`docs/07`). Our own honesty test in
  `docs/04` shows what happens without one.
- **It does not make a small model smart.** A 1.5B model writes short, simple replies well and fails at long, careful reasoning.
- **It does not make output safe.** A person should read anything that matters before it goes to a customer.
- **It is not magic on little or messy data.** Garbage in, a very faithful copy of the garbage out.

## About the style checker

`tools/style_check.py` counts visible rules: a greeting, a sign off, a length, banned words. It cannot tell whether
a reply is warm, funny, correct or kind. Passing every check does not mean "sounds like you". It means "followed your
visible rules". You still read the side by side answers.

## About the numbers in these docs

Times, memory and losses are from one machine, one afternoon, one small dataset, and they will differ on yours.
Other hardware, a busy Mac with many apps open, and a different dataset all change them.

## Privacy

Training happens on your computer. The base model is downloaded from Hugging Face once. Your examples are not
uploaded by this kit. Do not publish an adapter you trained on private data: it can leak what it learned. Do not
commit your examples, adapters or models to a public repository (the `.gitignore` already blocks `work/` and
`*.safetensors`).

## Licences

The kit is MIT. The base model used here, Qwen2.5 1.5B Instruct, is released under Apache 2.0. Check the licence of any
other model you choose before using its output commercially.
