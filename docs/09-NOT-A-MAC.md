# Not on an Apple Silicon Mac? Read this

**This kit's training path is tested only on a Mac with Apple Silicon (an M4 with 16 GB of memory).** Apple's MLX
runs on Apple Silicon. A Windows PC or an Intel Mac cannot run it. We have **not** tested anything below.

## What still works on any computer (standard Python 3.10 or newer, tested on 3.10 and 3.14)

- `tools/build_dataset.py`, `tools/check_data.py`, `tools/style_check.py` use only the standard library.
  They turn your examples into the common "messages" chat format and check them.
- The prompts in `prompts/` and the docs apply to any LoRA tool.

## Where to train instead (UNTESTED by us, pointers only)

| Option | What it is | Check before you trust it |
| --- | --- | --- |
| Hugging Face PEFT | The widely used Python library for LoRA, Apache 2.0 licence | Needs a computer with a supported GPU, or a rented one. Read its own docs. |
| Unsloth | A project aimed at faster, lower memory fine tuning, Apache 2.0 licence | Read what hardware it supports today. |
| Axolotl | A configuration driven fine tuning tool, Apache 2.0 licence | Needs a GPU setup. |
| A rented cloud GPU | You rent time on a graphics card | Never upload private customer data you have not cleaned. See `docs/02`. |
| Hosted fine tuning from an AI company | The company trains it for you on their servers, for a fee | Your examples go to that company. Read its data policy first. |

Links, all public: `github.com/huggingface/peft`, `github.com/unslothai/unsloth`,
`github.com/axolotl-ai-cloud/axolotl`, and OpenAI's fine tuning guide at
`platform.openai.com/docs/guides/fine-tuning`.

## Using this kit's data files with another tool

`train.jsonl`, `valid.jsonl` and `test.jsonl` use the `{"messages": [...]}` chat layout. Many tools read that layout,
but field names and chat templates differ. **We have not tried them in any other tool.** Check the tool's
dataset page before you rely on it.

## Honest note on the claim "you cannot do this to ChatGPT or Claude"

You cannot download those models and train them on your own computer, because their weights are not released.
Some companies sell hosted fine tuning of some of their models. That is a different path from this kit, with
different costs and a data policy of its own.
