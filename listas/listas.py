import os
from functools import lru_cache
from pathlib import Path

import lark

BASE = Path(__file__).parent
ANSWER = BASE / "grammar_answer.lark"
STUDENT = BASE / "grammar.lark"

if os.environ.get("ANSWER_KEY", "").lower() == "1":
    TEST_FILE = ANSWER if ANSWER.exists() else STUDENT
else:
    TEST_FILE = STUDENT


@lru_cache()
def grammar(lang: str):
    start = f"{lang}list"
    return lark.Lark(TEST_FILE.read_text(), start=start, parser="earley")


def validate(src: str, lang: str) -> bool:
    try:
        grammar(lang).parse(src)
        return True
    except lark.exceptions.LarkError as error:
        print("Erro:", error)
        return False
