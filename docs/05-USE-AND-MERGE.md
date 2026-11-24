# Use it, or merge it into one model

You have a trained adapter in `work/adapter/best` (about 20 MB). Three ways to use it.

## 1. Chat with it (adapter stays separate)

```bash
.venv/bin/python -m mlx_lm chat --model mlx-community/Qwen2.5-1.5B-Instruct-4bit --adapter-path work/adapter/best
```

The base model is the same file as always. The adapter is the thin binder. Remove `--adapter-path` and you are
talking to the plain model again. One base model can carry many adapters: a voice for support, one for sales.

**Always give it the same kind of system message you trained with** (your role line and fact sheet). In an earlier
run of ours (a first version of the sample data), the trained model scored 0 of 6 on style when we sent it no system
message at all, and one reply even signed off as "Qwen at Alibaba Cloud". With the role line present it held. If your
training examples had a system message, your real use needs it too.

## 2. Use it from your own Python

```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Qwen2.5-1.5B-Instruct-4bit", adapter_path="work/adapter/best")
messages = [{"role": "system", "content": open("data/FACT-SHEET.txt").read()},
            {"role": "user", "content": "Hi, it's Priya. Are you open this Sunday?"}]
prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
print(generate(model, tokenizer, prompt=prompt, max_tokens=160))
```

This is how `tools/compare.py` works, so it is tested.

## 3. Merge into one standalone model (careful, there is a trap)

```bash
.venv/bin/python tools/fuse.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
  --adapter-path work/adapter/best --save-path work/fused-16bit
```

**The trap we hit and measured:** merging into the compressed 4 bit model with the plain fuse command gave a model that
**lost the voice completely: 0 of 10 style checks**, while the adapter on its own scored 10 of 10. Merging with
`--dequantize` kept it: **10 of 10**, and 3 of 3 on the "let me check" test. The price is size: the merged folder is
about 2.9 GB instead of 0.85 GB. We think the tiny change is rounded away when it is squeezed back into 4 bit numbers.
We did not prove that cause. `tools/fuse.py` always uses `--dequantize`.

### Test the merged model before you trust it

```bash
.venv/bin/python tools/compare.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
  --fused-model work/fused-16bit --data work/data --card data/style-card.bluebird.json --out work/fusedexam
```

You need a free 6 GB of disk to merge. `docs/10` covers other problems.

## Keep it private

An adapter trained on your private examples can reveal what it learned. Do not upload or share it unless the
examples were safe to publish. This kit's `.gitignore` blocks `work/` and `*.safetensors` so you do not commit it by accident.

## Sharing or selling

Check the licence of the base model first. The one used here, Qwen2.5 1.5B Instruct, is Apache 2.0, which allows
commercial use with its conditions. Read it, we are not lawyers.
