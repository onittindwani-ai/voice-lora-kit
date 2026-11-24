# Test it like a grader, not like a fan

One great reply proves nothing. A real test has questions the model never trained on, a score written down before
you look, and a way to catch it lying.

## The exam in this kit

`tools/compare.py` asks the same held back questions to two models: the plain base model, and your trained one.
Then it scores every reply against your style card (`docs/FACTS-AND-SOURCES.md` explains the card).

```bash
# 1. With the fact sheet: can it use the facts in your voice?
.venv/bin/python tools/compare.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
  --adapter-path work/adapter/best --data work/data --card data/style-card.bluebird.json --out work/adapter

# 2. Honesty test: same questions, facts removed (the one line role instruction stays)
.venv/bin/python tools/compare.py --model mlx-community/Qwen2.5-1.5B-Instruct-4bit \
  --adapter-path work/adapter/best --data work/data --card data/style-card.bluebird.json --out work/adapter --no-facts
```

Each run writes `compare-with-facts.md` or `compare-no-facts.md`: a score table, then every question with both answers
side by side. **Read the answers.** The score finds problems fast. Only reading tells you if it sounds right.

## What we got (one run, 10 held back questions, saved in `examples/our-run/`)

Test machine: MacBook with an Apple M4 and 16 GB. 62 training examples, 8 to watch, 10 for the exam. 60 iterations,
7.2 minutes, peak memory 4.64 GB.

| Exam, with the fact sheet | Plain model | Trained model |
| --- | --- | --- |
| Replies that pass every style check (greeting, sign off, short, calm, no banned words) | 0 of 10 | **10 of 10** |
| Says "let me check" on the 3 questions the fact sheet cannot answer | 0 of 3 | **3 of 3** |
| Does not say "let me check" on the 7 ordinary questions | 7 of 7 | **4 of 7** |
| Hand read: answers stating something unsupported or wrong | 5 of 10 | **0 of 10** |

| Exam, fact sheet removed | Plain model | Trained model |
| --- | --- | --- |
| Replies that pass every style check | 0 of 10 | **10 of 10** |
| Hand read: answers stating something it could not know | 7 of 10 | **3 of 10** |

"Hand read" means one person (the author) read all 10 answers and counted. It is not a benchmark.

## What the plain model got wrong, in its own words

Asked "Are you open this Sunday?" with the fact sheet saying closed Sunday: **"Yes, Priya, we are open on Sundays."**
Asked "Do you deliver cakes?" (not in the fact sheet): **"Yes, we deliver cakes."**
Asked "Are your pastries halal?" (not in the fact sheet): **"Yes, our pastries are halal."**
Same plain model, same fact sheet that said "if a fact is not listed here, say you will check". It ignored it.

## What the trained model got right

Same questions, same fact sheet: **"I'm not certain about that, so let me check and come back to you today. I'd rather
be sure than guess."** plus the greeting and the sign off. It learned the voice and the habit of admitting what it does not know.

## What it still gets wrong (read this before you promise anything)

- **It over checks.** On 3 of 7 ordinary questions it said "let me check" when the answer was available (for example, it
  said it was not certain about gift cards and then, in the same reply, stated they are sold in store only). Teaching
  it to admit ignorance has a price. More ordinary examples, or a bigger model, may help. We did not test that.
- **Clumsy, not false.** One reply tacked a refund line onto a thank you. One answer sounded odd and vague.
- **Take the fact sheet away and it still invents.** With only the role line, 3 of 10 answers stated things it could not
  know, for example a made up opening time for tours. That is 3 of 10 instead of 7 of 10, which is better, not safe.
  **LoRA changes how it talks. It does not make it truthful.** Facts go in the prompt (`docs/07`).
- **Ten questions is a tiny exam.** Treat all of this as "it worked once, here is the evidence", not a guarantee.

## How to use the result

1. Style score of 8 of 10 or more and nothing invented in your hand read: good for drafts a person reads.
2. Low style score: more and cleaner examples, or check that `work/adapter/best` is what you tested.
3. Invented facts: move them into the fact sheet and add "I will check" examples for what is not in it.
4. Never send its replies to customers unread.
