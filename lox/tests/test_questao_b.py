from datetime import date

import rich

from lox.ast import Array, Assign, Binary, Expr, Literal  # type: ignore
from lox.lox import parse as raw_parse
from lox.token import Token, TokenType


def lox(x):
    if isinstance(x, Expr):
        return x
    return Literal(x)


def array(*xs):
    return Array([lox(x) for x in xs])


def attr(obj):
    data = vars(obj)
    name, value = data.popitem()
    if data:
        msg = f"{obj} deveria ter apenas 1 atributo"
        raise ValueError(msg)
    return value


def check(src, expect):
    got = parse(src)

    rich.print("Fonte:")
    print("    " + src)
    rich.print("\n\nAST")
    rich.print(got)
    rich.print("\n\nEsperado")
    rich.print(expect)

    assert got == expect


def parse(src: str):
    program = raw_parse(f"print {src};")
    return attr(attr(program)[0])  # type: ignore


def test_parse_array_vazia():
    check("[]", array())


def test_parse_array_simples():
    check('["a", "b", "c"]', array("a", "b", "c"))


def test_parse_array_aninhada():
    check('["a", ["b", ["c"]]]', array("a", array("b", array("c"))))


def test_aceita_atribuicao_dentro_da_array():
    check('[x = "a", "b", "c"]', array(Assign("x", lox("a")), "b", "c"))


def test_aceita_datas():
    check("'2025-11-27", lox(date(2025, 11, 27)))


def test_aceita_arrays_com_datas():
    check(
        "['2025-11-27, '2024-01-01]",
        array(lox(date(2025, 11, 27)), lox(date(2024, 1, 1))),
    )


def test_aceita_subtracao_de_datas():
    check(
        "'2025-11-27 - '2024-01-01",
        Binary(
            lox(date(2025, 11, 27)),
            Token(TokenType.MINUS, "-", 1),
            lox(date(2024, 1, 1)),
        ),
    )
