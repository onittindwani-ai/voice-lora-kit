# Prompt 3: audit my examples before I train

Run this after build_dataset.py and before train.py. It is the cheapest hour you will ever save.

```
Read work/data/train.jsonl. Act like a strict editor, not a cheerleader.
Report these, with counts and line numbers:
1. Replies that break my own style card (run tools/style_check.py on each).
2. Pairs where two examples teach opposite habits (for example one signs off with a name, another does not).
3. Replies that state a fact (a price, a time, a policy). List each fact and check it against my fact sheet.
   A fact that is wrong or out of date is the worst thing to teach.
4. Near duplicates (the same question in different words with the same reply).
5. Topics I have too few examples of. Name them.
6. Any private detail left (names, numbers, emails, addresses).
Then propose the smallest set of fixes. Do not rewrite my replies. Show me the old line and your suggestion,
and let me decide.
```

Why: the model copies the mess along with the good parts. That is common practitioner advice. This kit did
not test messy data against clean data, so treat it as a strong rule of thumb, not a measured result. See docs/06.
