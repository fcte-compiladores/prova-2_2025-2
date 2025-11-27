import os
import sys
import time
from typing import TYPE_CHECKING

from .env import Env

try:
    assert os.environ.get("ANSWER_KEY", "").lower() == "1"
    from .interpreter_answer import exec
    from .parser_answer import parse
except (ImportError, AssertionError):
    from .interpreter import exec
    from .parser import parse


if not TYPE_CHECKING and os.environ.get("ANSWER_KEY") == "1":
    from .interpreter_answer import exec
    from .parser_answer import parse
else:
    from .interpreter import exec
    from .parser import parse


def main():
    if len(sys.argv) == 1:
        return repl()
    elif len(sys.argv) == 2:
        return run_file(sys.argv[1])
    else:
        exit("Uso: pylox [ NOME DO ARQUIVO ]")


def run_file(path: str):
    with open(path) as f:
        source = f.read()

    lox = Lox()
    lox.run(source)


def repl():
    lox = Lox()

    while True:
        try:
            cmd = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            break

        try:
            lox.run(cmd)
        except Exception as error:
            typ = type(error).__name__
            print(f"{typ}: {error}")


class Lox:
    def __init__(self):
        from lox.runtime import NativeFunction

        self.ctx = Env()
        self.ctx.define("clock", NativeFunction(time.time, 0))

    def run(self, src: str):
        ast = parse(src)
        exec(ast, self.ctx)


if __name__ == "__main__":
    main()
