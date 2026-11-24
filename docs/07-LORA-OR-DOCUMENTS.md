# LoRA, a fact sheet, or documents? Pick the right tool first

Most people who ask for "fine tuning" really want one of three different things. Picking the wrong one is the
most expensive mistake in this whole kit.

| You want the AI to... | Use | Why |
| --- | --- | --- |
| Sound like you: your tone, greeting, sign off, length, habits | **LoRA** (this kit) | Style is a pattern across many examples. Training is how a model absorbs a pattern. |
| Know your facts: prices, hours, policies, product details | **A fact sheet in the prompt**, or documents it reads each time | Facts change. A fact baked into a model cannot be edited, and the model may still blur it. |
| Answer from a large pile of documents | **Documents the AI searches** (often called RAG) | The pile can be bigger than any prompt, and you can update it without retraining. |
| Follow one simple rule once | **A better prompt** | Free, instant, and the first thing to try before anything else. |

## The honest rule

**LoRA teaches style. A fact sheet supplies facts.** Use both together: a fact sheet in the prompt, and a LoRA
trained on replies that already use that fact sheet correctly. That is exactly how the sample in this kit works:
every training example carries the same fact sheet (`data/FACT-SHEET.txt`) and a reply that uses it in Maya's voice.

## Try these before you train anything

1. Put 3 of your best replies in the prompt as examples and ask for a new one. Often good enough.
2. Add your fact sheet. Check again.
3. Only if you need the voice on every reply, hands off, at scale, or on a small model that follows long
   instructions badly, train a LoRA.

This order is practitioner advice, not a measured result.

## What the kit's own honesty test shows

`tools/compare.py --no-facts` asks the trained model the same questions **without** the fact sheet.
Read `docs/04-TEST-LIKE-A-GRADER.md` for what happened in our run. If the model sounds like Maya but states a
time or price that is not true, that is the lesson: it learned the voice, and it did not learn the facts.

## Other things people hope LoRA does, and the truth

- "Make it smarter." No. A small model stays a small model.
- "Teach it my new product." Give it the product page to read. Retraining for every product change is the wrong job.
- "Make it safe." No. Keep a person reading anything that matters.
- "Give it a personality." Yes, to the extent your examples show one.
