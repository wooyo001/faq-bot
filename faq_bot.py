"""faq-bot: a tiny FAQ chatbot using TF-IDF and cosine similarity (standard library only).

Chat:      python faq_bot.py
Evaluate:  python faq_bot.py --eval
"""
import argparse, json, math, re
from collections import Counter
from pathlib import Path

DATA = Path(__file__).parent / "data"
STOPWORDS = {"a", "an", "the", "i", "my", "me", "do", "does", "how", "can", "to", "is", "are",
             "for", "of", "in", "on", "at", "and", "or", "where", "when", "what", "will", "get"}


def stem(word):
    for suffix in ("ing", "ers", "er", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def tokenize(text):
    return [stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS]

class FAQBot:
    def __init__(self, faq, threshold=0.2):
        self.faq, self.threshold = faq, threshold
        docs = [tokenize(item["question"]) for item in faq]
        n = len(docs)
        df = Counter(w for d in docs for w in set(d))
        self.idf = {w: math.log((1 + n) / (1 + c)) + 1 for w, c in df.items()}
        self.vectors = [self._vector(d) for d in docs]

    def _vector(self, tokens):
        tf = Counter(tokens)
        vec = {w: c * self.idf[w] for w, c in tf.items() if w in self.idf}
        norm = math.sqrt(sum(v * v for v in vec.values()))
        return {w: v / norm for w, v in vec.items()} if norm else {}

    def ask(self, query):
        """Return (faq_id or None, score). None means 'no good match'."""
        q = self._vector(tokenize(query))
        scores = [sum(v * q.get(w, 0) for w, v in vec.items()) for vec in self.vectors]
        best = max(range(len(scores)), key=scores.__getitem__)
        if scores[best] < self.threshold:
            return None, scores[best]
        return self.faq[best]["id"], scores[best]


def evaluate(bot, tests):
    correct, failures = 0, []
    for t in tests:
        got, score = bot.ask(t["query"])
        if got == t["expected_id"]:
            correct += 1
        else:
            failures.append((t["query"], t["expected_id"], got, round(score, 2)))
    return correct / len(tests), failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", action="store_true", help="measure accuracy on data/test.json")
    ap.add_argument("--threshold", type=float, default=0.2)
    a = ap.parse_args()
    faq = json.loads((DATA / "faq.json").read_text())
    bot = FAQBot(faq, a.threshold)
    if a.eval:
        tests = json.loads((DATA / "test.json").read_text())
        acc, failures = evaluate(bot, tests)
        print(f"Accuracy: {acc:.0%} on {len(tests)} test questions (threshold {a.threshold})")
        for q, exp, got, s in failures:
            print(f"  WRONG: '{q}' expected {exp}, got {got} (score {s})")
        return
    print("FAQ bot. Type a question (or 'quit').")
    by_id = {f["id"]: f for f in faq}
    while True:
        q = input("> ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        fid, score = bot.ask(q)
        print(by_id[fid]["answer"] if fid else "Sorry, I don't know the answer to that.")


if __name__ == "__main__":
    main()
