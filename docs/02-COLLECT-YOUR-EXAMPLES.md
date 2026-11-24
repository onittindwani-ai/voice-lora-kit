# Collect your examples: the part that decides the result

The model copies what you show it. The examples are the whole teacher, so this is where the quality comes from.

## How many

| Rows | What to expect |
| --- | --- |
| Under 20 | `build_dataset.py` stops. Not enough to learn a pattern. |
| 20 to 49 | It will train. The result may be thin. The tool warns you. |
| **50 to 100** | A good first target. The sample in this kit has 70 (58 to train, 6 to watch, 6 for the final exam). |
| More | Only if the extra rows are as good as the first ones. Add more of the topics you are weakest at, not more of the same. |

These numbers are a sensible starting range from practitioner experience and this kit's single test. They are not a
law. The QLoRA paper reports that fine tuning on a small, high quality dataset can give strong results, which is the
same idea: quality beats quantity.

## What a good example looks like

1. **A real message and a reply you are proud of.** Not your busiest, laziest or angriest day.
2. **Your real wording.** Your greeting, your sign off, your length. Do not polish. The aim is to copy you, not improve you.
3. **A reply that uses facts correctly.** If a price or a time is wrong in an example, the model learns the wrong
   habit of stating prices. Keep a fact sheet and check each reply against it (`prompts/03`).
4. **Variety.** Easy questions, tricky ones, complaints, thanks, and some "I do not know, let me check" replies. If every example is
   a happy answer, the model will not know how to say "I am not sure".
5. **Consistent habits.** If you sign off with your name in half the replies and not in the others, the model will do
   both at random. Pick one habit and keep it in the examples.

## What to leave out

- Private details: other people's names, phone numbers, emails, addresses, order numbers, card digits.
  `build_dataset.py` scans for phone numbers, emails, card style numbers and web links and stops until you fix or
  accept them. It cannot spot a name or an address, so read your own data once.
- Replies you would not want copied: rude, rushed, one word, "see attached", or wrong.
- Anything covered by a confidentiality promise. When in doubt, replace it with a made up equivalent like the sample does.

## The format

A spreadsheet saved as CSV with two columns: `customer_message` and `reply` (`templates/examples-template.csv`).
If your columns have other names, use `--message-col` and `--reply-col`.

## The fact sheet (optional but recommended)

If your replies use facts (hours, prices, policies), put them in a short text file and pass it with `--system-file`.
It is placed in every example, so the model learns to **use** the fact sheet instead of guessing.
See `docs/07-LORA-OR-DOCUMENTS.md` and `templates/fact-sheet-template.txt`.

## The three files you get

| File | Job | Rule |
| --- | --- | --- |
| `train.jsonl` | The lessons | The model learns from these |
| `valid.jsonl` | The practice quiz | Watched during training to see if it is really learning |
| `test.jsonl` | The final exam | Training never sees it. `check_data.py` errors if a question appears in two files |
