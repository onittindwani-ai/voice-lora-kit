---
description: Run the before and after exam, with and without the fact sheet
---
Run `python3 tools/compare.py --model <the model used for training> --adapter-path work/adapter --card <the style card>`
and then the same command with `--no-facts`. Report both pass rates, quote the two weakest trained answers, and say
which facts the model made up in the no fact sheet run. Use `prompts/04-READ-MY-RESULTS.md` as the guide.
