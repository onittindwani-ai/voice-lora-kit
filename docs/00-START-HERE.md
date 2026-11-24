# Start here: what LoRA is, in one picture

## The new hire

Imagine you hire a brilliant new person who has read the whole internet. They know a little about everything.
But they write to your customers like a Wikipedia article that has just had bad news.

You have three ways to fix that.

1. **A sticky note every morning** ("be friendly, keep it short"). Cheap, but you have to hand it over every
   single time, and it only goes so far. That is **prompting**.
2. **Send them back to university for four years** so they become a different person. Powerful, but it costs a fortune
   and you cannot undo it. That is **full fine tuning**.
3. **A short practice week.** They study 60 of your best real replies, practise, and come out writing the way your
   company writes. Their degree is untouched. What changed fits in a thin binder you can slip in or out of their bag.
   That is **LoRA**.

## Now the real words

| In the picture | In real life |
| --- | --- |
| The new hire | A free, open AI model (here Qwen2.5 1.5B, about 1.5 billion numbers) |
| Their degree | The model's weights. LoRA **freezes** them, so they never change |
| The practice week | Training, on your examples, on your own Mac |
| The thin binder | The **adapter**: a small file (about 20 MB here, next to a model of about 840 MB). In our run it trained only 0.342 percent of the numbers (5.276M of 1,543.714M) |
| Slipping the binder in or out | Load or remove the adapter. One base model, as many voices as you like |
| Gluing the binder into their brain | **Fusing**: merging the adapter into one standalone model (`docs/05`) |

The idea comes from a 2021 research paper, "LoRA: Low-Rank Adaptation of Large Language Models" (arXiv 2106.09685). For a
175 billion number model it reports about 10,000 times fewer trainable numbers and about 3 times less graphics
memory than retraining everything, with no extra delay when the model runs.

## What it changes, and what it does not

The practice week teaches **how they talk**: greeting, sign off, length, habits.
It does **not** teach **what is true**. Their prices, hours and policies must be handed to them on a fact sheet.
That one fact is the difference between a LoRA that works and one that confidently makes things up.
Read `docs/07-LORA-OR-DOCUMENTS.md` before you collect a single example.

## What you will do in this kit

1. `docs/01` Check your Mac can do it.
2. `docs/02` Collect 50 to 100 of your best real examples.
3. `docs/03` Train. About 10 minutes, depending on your Mac and what else is open.
4. `docs/04` Take a before and after exam, with and without the fact sheet.
5. `docs/05` Use it, or merge it into one model.
6. `docs/06` Read the 10 mistakes first. Each one has a real symptom and a fix.

## Quick start with an AI assistant

Open Claude Code or Codex in this folder and paste `prompts/00-QUICK-START-FOR-CLAUDE-CODE.md`.
It will do the steps for you, in plain words, and ask before it installs anything.

## Say it out loud

LoRA is said "LOH-rah".
