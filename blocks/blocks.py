import os
from pathlib import Path

import lark

BASE = Path(__file__).parent
ANSWER = BASE / "grammar_answer.lark"
STUDENT = BASE / "grammar.lark"

if os.environ.get("ANSWER_KEY", "").lower() == "1":
    TEST_FILE = ANSWER if ANSWER.exists() else STUDENT
else:
    TEST_FILE = STUDENT


grammar = lark.Lark(TEST_FILE.read_text(), start="start", parser="earley")


def validate(src: str) -> bool:
    try:
        grammar.parse(src)
        return True
    except lark.exceptions.LarkError:
        return False
