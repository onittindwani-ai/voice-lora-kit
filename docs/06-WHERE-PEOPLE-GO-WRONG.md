# Where people go wrong: 10 mistakes, with symptoms and fixes

Each mistake carries an evidence label. **TESTED** means we saw it in this kit's own runs. **TOOL** means a tool in
this kit catches it and a test proves the tool works. **ADVICE** means common practitioner advice that we did not measure.

## 1. Expecting it to learn your facts (TESTED)

- **Symptom:** it sounds exactly like you and states a wrong price, hour or policy.
- **Evidence:** with the fact sheet removed, the trained model stated something it could not know in 3 of 10 answers
  (the plain model, 7 of 10). Voice 10 of 10, truth still not guaranteed.
- **Fix:** put facts in a fact sheet in the prompt, and train on examples that use it (`docs/07`).

## 2. Training too long (TESTED)

- **Symptom:** your examples come back almost word for word, or answers get oddly rigid.
- **Evidence:** in every run the validation score was best at iteration 25 to 30 (about 2 passes through 62 examples) and then
  got worse: 3.178, best 1.018 at iteration 30, then 1.385 at 60. In an earlier 150 iteration run it went from a best of
  0.943 to 1.823 while the training loss fell to 0.001. The model was memorising.
- **Fix:** keep `--save-every` and `--steps-per-eval` small, and use the folder called `best` that `train.py` writes.

## 3. Merging into the compressed model (TESTED)

- **Symptom:** the merged model forgot your voice.
- **Evidence:** plain `fuse` into the 4 bit model: 0 of 10 style checks. With `--dequantize`: 10 of 10 (`docs/05`).
- **Fix:** use `tools/fuse.py`, and test the merged model with `compare.py --fused-model`.

## 4. Judging by one good reply (TESTED)

- **Symptom:** "it works!" after two lucky tries.
- **Evidence:** in our runs one answer was perfect while the next claimed a delivery service that does not exist.
- **Fix:** an exam of held back questions, scored the same way before and after (`docs/04`).

## 5. The same question in training and in the exam (TOOL)

- **Symptom:** a great score that falls apart on real customers.
- **Fix:** `tools/build_dataset.py` splits once with a fixed seed, `tools/check_data.py` fails if a question appears in two files.

## 6. No "I do not know" examples (TESTED, with a caution)

- **Symptom:** it guesses confidently when asked something outside your fact sheet.
- **Evidence:** the plain model said yes to delivery and halal, neither in the fact sheet. After training on examples that
  say "let me check and come back today" (23 of the 80 sample rows), the trained model did so on 3 of 3 such questions.
  Our first version of the sample had fewer of them and the trained model still guessed on some. We changed the data and the
  exam between those versions, so read this as a strong hint, not proof.
- **Fix:** mark such rows `unknown` in a `kind` column. The exam checks them (`docs/04`).

## 7. Too many "I do not know" examples (TESTED)

- **Symptom:** it hides behind "let me check" even when the answer is in the fact sheet.
- **Evidence:** on 3 of 7 ordinary questions the trained model said it needed to check. The price of teaching honesty.
- **Fix:** balance the examples, and read the answers. We did not find the best balance. 23 of 80 may be too many.

## 8. Messy or inconsistent examples (ADVICE)

- **Symptom:** it signs off sometimes, forgets the greeting sometimes, sounds different every time.
- **Why:** it copies the inconsistency. Half the examples with a sign off and half without teaches "flip a coin".
- **Fix:** one habit, kept in every example. Write the style card from your own replies (`prompts/02`) and let
  `style_check.py` flag the ones that break it.

## 9. Private data in the examples (TOOL)

- **Symptom:** the model repeats a name, a phone number or an address.
- **Fix:** `build_dataset.py` stops on emails, phone numbers, card style numbers and web links. It cannot see names or
  addresses, so read your own data once. Never share an adapter trained on private data.

## 10. Reaching for training when a prompt would do (ADVICE)

- **Symptom:** a weekend spent training, and the result is no better than three good examples pasted into a prompt.
- **Fix:** try the prompt and the fact sheet first (`docs/07`). Train when you need the voice everywhere, every time, hands off.

## The short version

Clean examples, a fact sheet, a held back exam, the best checkpoint, and a person reading before anything is sent.
