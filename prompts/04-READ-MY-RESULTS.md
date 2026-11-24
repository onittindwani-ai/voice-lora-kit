# Prompt 4: read my results in plain words

```
Read these files from my last run:
- work/adapter/run-summary.json
- work/adapter/compare-with-facts.md
- work/adapter/compare-no-facts.md   (only if I ran the honesty test)

Explain to me like I am not technical:
1. Did training fit on this computer? (memory, time, adapter size)
2. Did the validation number go down and then back up? If the best iteration is far below the last one,
   say I trained too long and give the exact --iters to use next.
3. How many replies passed every style check before and after?
4. Read 3 side by side answers and tell me honestly if the trained one sounds more like me,
   and where it still does not.
5. In the honesty test, which facts did the model make up? Quote them.
6. Give me ONE next step: train again with a specific change, add examples of a specific kind, or stop.
Do not say "great result" unless the numbers support it.
```
