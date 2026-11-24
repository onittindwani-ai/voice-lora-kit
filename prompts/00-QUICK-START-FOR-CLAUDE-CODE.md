# Quick start: paste this into Claude Code or Codex

Open Claude Code (or Codex) inside this folder, then paste everything in the box below.

```
You are helping me teach a small open AI model to write in my own voice, using LoRA,
on this Mac. This folder is a kit. Read README.md and docs/00-START-HERE.md first.

Rules for this whole job:
- Everything stays on this computer. Never upload my examples, my model or my adapter anywhere.
- Ask before installing anything, and tell me how much disk it uses.
- Stop and tell me if free disk drops under 5 GB.
- Use only the commands in docs/03-TRAIN-STEP-BY-STEP.md. Do not invent flags.
- Explain each step in plain words before you run it, like I have never done this.

Do this in order:
1. Run: python3 tools/check_machine.py. Tell me the verdict in one sentence.
2. Help me set up a Python 3.11 or 3.12 environment with mlx-lm (docs/03). Show me the exact commands first.
3. Ask me what kind of writing I want to teach (customer replies, sales emails, social posts).
   Then help me collect 50 to 100 of my real best examples into a CSV using templates/examples-template.csv.
   Use prompts/01-GATHER-MY-BEST-EXAMPLES.md. Remove private details before we continue.
4. Help me write my style card (prompts/02-WRITE-MY-STYLE-CARD.md) so we can measure the result.
5. Run tools/build_dataset.py and tools/check_data.py. Fix anything they report.
6. Run tools/train.py with the default settings. Tell me what you see while it runs.
7. Run tools/compare.py and show me the before and after in plain words.
   Say what improved, what did not, and whether I should train again or stop.
8. Remind me that this teaches STYLE, not facts. For facts we give the model a fact sheet (docs/07).
```

That is the whole job. If anything fails, paste the error and say "use docs/10-TROUBLESHOOTING.md".
