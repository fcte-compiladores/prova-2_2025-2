import io
from contextlib import redirect_stdout

import rich

from lox.lox import Lox


def run(src):
    lox = Lox()
    lox.run(src)


def check(src, expect):
    rich.print("Fonte:")
    print("\n".join("  " + line for line in src.splitlines()))

    try:
        with redirect_stdout(io.StringIO()) as f:
            run(src)
            got = f.getvalue()
    except Exception as e:
        got = f"{e.__class__.__name__}: {e}"

    rich.print("\nObtido")
    print("\n".join("  " + line for line in got.splitlines()))

    rich.print("\n\nEsperado")
    print("\n".join("  " + line for line in expect.splitlines()))

    assert got.replace("'", '"').rstrip() == expect.rstrip()


def test_imprime_array_vazia():
    check("print [];", "[]")


def test_imprime_array_simples():
    check('print ["a", "b", "c"];', "[a, b, c]")


def test_imprime_array_aninhada():
    check('print ["a", ["b", ["c"]]];', "[a, [b, [c]]]")


def test_imprime_atribuicao_dentro_da_array():
    check('var x;\nprint [x = "a", "b", "c"];\nprint x;', "[a, b, c]\na")


def test_imprime_datas():
    check("print '2025-11-27;", "2025-11-27")


def test_imprime_arrays_com_datas():
    check(
        "print ['2025-11-27, '2024-01-01];",
        "[2025-11-27, 2024-01-01]",
    )


def test_imprime_subtracao_de_datas():
    check("print '2025-11-27 - '2024-01-01;", "696")
