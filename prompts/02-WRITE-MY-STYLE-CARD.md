# Prompt 2: write my style card

A style card turns "sounds like me" into rules a script can check. Without it, you judge the result by feel and
one lucky reply fools you.

```
Read my-examples.csv. Look only at the reply column.
Draft my style card as JSON in the format of templates/style-card-template.json.

Only include a rule if at least 90 percent of my replies already follow it. Measure it, do not guess.
Report your numbers like this: "greeting starts with Hi + name: 97 of 100".
Cover:
- how my replies start (a regex for the greeting)
- how they end (the exact sign off line, if I always use one)
- the longest a reply gets (max_words), with some room above my longest normal reply
- how many sentences the middle usually has (max_sentences_in_body)
- characters or phrases I never use (long dashes, "As an AI", "I apologize for any inconvenience")

Then run: python3 tools/style_check.py --card style-card.json on 5 of my replies and show me the output.
If one of my own replies fails a rule, tell me, and ask whether the rule or the reply is wrong.
Do not invent rules I do not follow.
```

What the card cannot do: judge warmth, humour or taste. It checks your visible habits. You read the
side by side answers and decide the rest. See docs/04-TEST-LIKE-A-GRADER.md.
