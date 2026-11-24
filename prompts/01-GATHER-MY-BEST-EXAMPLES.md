# Prompt 1: gather my best examples

Use this when you are not sure which of your old messages are good enough to learn from.

```
I want to teach an AI model to write the way I write. Help me build a CSV with two columns:
customer_message (what the other person wrote) and reply (what I wrote back).

Here is how I want you to work:
1. Ask me where my best writing lives (sent emails, chat replies, DMs, a notes file).
   I will paste a few at a time. Never ask me to connect an account.
2. For each pair I paste, keep it only if the reply is something I am proud of.
   Skip rushed, rude, one word or "see attached" replies.
3. Remove private details before saving: names of people other than the greeting, phone numbers,
   emails, addresses, order numbers, prices that are not public. Replace with something harmless.
4. Keep my real wording, my greeting, my sign off and my length. Do not "improve" my writing.
   The point is to copy me, not to polish me.
5. Keep the examples varied: different questions, different moods, some complaints, some thanks,
   some "I do not know, let me check" replies.
6. After every 10 pairs, tell me how many we have and what kinds are missing.
7. Stop at 50 to 100 pairs. Save to my-examples.csv in the format of templates/examples-template.csv.
```

Why this matters: the model copies what you give it, including your bad days. Fifty replies you are proud
of beat five hundred you are not. See docs/02-COLLECT-YOUR-EXAMPLES.md.
