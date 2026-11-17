import json, sys, pathlib
root = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(root))
from faq_bot import FAQBot, tokenize

faq = json.loads((root / "data" / "faq.json").read_text())

def test_tokenize_removes_stopwords():
    assert tokenize("How do I print?") == ["print"]

def test_exact_question_matches():
    bot = FAQBot(faq)
    assert bot.ask("How do I book a study room?")[0] == 9

def test_unrelated_question_returns_none():
    assert FAQBot(faq).ask("what is the weather today")[0] is None
