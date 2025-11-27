import random
from string import ascii_lowercase

import blocks
import pytest

N_BRUTE_FORCE_TESTS = 100


def st(size: int):
    if size <= 1:
        return "e" + random.choice([" ", ""]) + ";"
    if random.choice([True, False]):
        n = random.randint(1, size - 1)
        return st(n) + st(size - n)
    else:
        return "{" + st(size - 2) + "}"


def check_valid(src: str):
    if not blocks.validate(src):
        assert blocks.validate(src), (
            f"Entrada esperada como válida não foi aceita: {src}"
        )


def check_invalid(src: str):
    if blocks.validate(src):
        assert not blocks.validate(src), (
            f"Entrada esperada como inválida foi aceita: {src}"
        )


@pytest.mark.parametrize("src", ["e;", "{e;}", "{e;}{e;}", "{{e;}}"])
def test_bons_exemplos(src: str):
    check_valid(src)


@pytest.mark.parametrize("src", ["", "{}", "}{", "{", "}", "{}}"])
def test_maus_exemplos(src: str):
    check_invalid(src)


def test_forca_bruta_a():
    n = N_BRUTE_FORCE_TESTS
    for i in range(n):
        src = st(i + 1)
        print(src)
        check_valid(src)


test_forca_bruta_b = test_forca_bruta_a
test_forca_bruta_c = test_forca_bruta_a
test_forca_bruta_d = test_forca_bruta_a


def test_forca_bruta_e():
    extra = ascii_lowercase.replace("e", "") + "{}" * 10
    n = N_BRUTE_FORCE_TESTS
    for i in range(n):
        chars = list(st(i + 1))
        extra_char = random.choice(extra)
        pos = random.randint(0, len(chars))
        chars.insert(pos, extra_char)
        src = "".join(chars)
        print(src)
        check_invalid(src)


test_forca_bruta_f = test_forca_bruta_e
test_forca_bruta_g = test_forca_bruta_e
test_forca_bruta_h = test_forca_bruta_e
