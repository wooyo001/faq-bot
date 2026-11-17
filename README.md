# faq-bot

A small FAQ chatbot written in plain Python (no libraries needed). You ask a question, and it finds the closest matching FAQ entry using TF-IDF and cosine similarity. It also includes an evaluation script that measures how accurate the bot is.

## Run it
```bash
python faq_bot.py            # chat with the bot
python faq_bot.py --eval     # measure accuracy on data/test.json
```
(On Mac, use `python3`.)

## How it works
1. Each FAQ question is split into words, with common words ("the", "how", "do") removed.
2. Words are weighted by how rare they are (TF-IDF), so rare words matter more.
3. Your question is compared to every FAQ question using cosine similarity.
4. The best match is returned. If the score is too low, the bot says it doesn't know.

## Baseline result
```
Accuracy: 77% on 22 test questions (threshold 0.2)
```
The test set includes paraphrases and two off-topic questions that should get "I don't know".

## Error analysis
Most failures come from word forms the bot treats as different words: "applying" vs "apply", "printer" vs "print", "wifi" vs "Wi-Fi". Another failure: a question about "timetable for classes" matched the exam timetable entry because the wrong word was weighted most.

## Ideas to improve it (each one can be measured with `--eval`)
- [ ] Add stemming so "applying" and "apply" match
- [ ] Add a small synonym list ("wifi" = "wi-fi" = "network")
- [ ] Tune the threshold and plot accuracy against it
- [ ] Add more test questions and report results per FAQ entry
- [ ] Replace TF-IDF with sentence embeddings and compare

## Note
The FAQ answers in `data/faq.json` are sample text. Replace them with real information for your own use.

## Tests
```bash
pip install pytest
pytest -q tests
```

## License
MIT
