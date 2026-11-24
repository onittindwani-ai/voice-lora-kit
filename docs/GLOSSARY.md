# Glossary: every word in plain English

| Word | Plain meaning |
| --- | --- |
| **Model** | The AI brain. A big file of numbers learned from a huge amount of text. |
| **Base model** | The model before you change it. In this kit, the free Qwen2.5 model. |
| **Open model** | A model whose files anyone can download and run. Only these can be trained at home. |
| **Fine tuning** | Teaching an existing model something extra with your own examples. |
| **LoRA** | Short for Low-Rank Adaptation, said "LOH-rah". Fine tuning where the big model stays frozen and you train a tiny add on layer. |
| **Adapter** | The tiny add on file LoRA produces. Here about 20 MB, next to a model of about 840 MB. |
| **QLoRA** | LoRA on a compressed (4 bit) model, to save memory. In mlx-lm, using a 4 bit model does this automatically. |
| **Quantized, 4 bit** | A compressed copy of a model that is smaller and a little less precise. |
| **Parameter** | One number inside the model. Models have millions to billions. |
| **Epoch** | One full pass through all your examples. |
| **Iteration (step)** | One small update, using a handful (the batch) of examples. |
| **Batch size** | How many examples the model looks at per step. |
| **Loss** | A score of how wrong the model is on its homework. Lower is better. |
| **Validation loss** | The same score on examples it has not trained on. The honest one. |
| **Overfitting** | The model memorises your examples instead of learning the pattern. Training loss keeps falling while validation loss rises. |
| **Held out / test set** | Examples kept back as a final exam. Training never sees them. |
| **Prompt** | What you send the model. |
| **System message** | Instructions placed before the question. In this kit it holds the fact sheet. |
| **Fused model** | The adapter merged into the base model, so you run one thing. |
| **RAG** | Letting the AI look up your documents each time it answers, instead of memorising them. |
| **Tokens** | Chunks of text the model reads. Roughly three quarters of a word each. |
| **Style card** | This kit's small JSON file that turns "sounds like me" into checkable rules. |
