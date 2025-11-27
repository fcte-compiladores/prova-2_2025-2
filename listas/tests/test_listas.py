import listas
import pytest
from lark import LarkError

GOOD_LISTS = ["[" + ", ".join(map(str, range(n))) + "]" for n in range(1, 10, 2)]
GOOD_PY_LISTS = [lst.replace("]", ", ]") for lst in GOOD_LISTS]
GOOD_JS_LISTS = [
    lst.replace(",", ",,").replace("[", "[,").replace("]", ",]")
    for lst in GOOD_PY_LISTS
]

JSON_LISTS = [
    "[]",
    "[e]",
    "[x, y, z]",
    "[[]]",
    "[[], []]",
    "[[1, 2], [3, [4]], e]",
]

PY_LISTS = [
    *JSON_LISTS,
    "[a, b, c,]",
    "[1, ]",
    "[[1,2,], [3,4,]]",
]


JS_LISTS = [
    *PY_LISTS,
    "[,]",
    "[x,,]",
    "[,,x]",
    "[1,, 2,, 3,]",
    "[,,[1,,2],,[3,,4],,]",
    "[1, [1,, 2,, 3,]]",
]

LISP_LISTS = [
    # "'()",
    # "' ( )",
    "'(e)",
    "'(x y z)",
    "'('())",
    "'('() '())",
    "'('(1 2) '(3 '(4)) e)",
]

LUA_LISTS = [
    *[src.replace("[", "{").replace("]", "}") for src in GOOD_LISTS],
    *[src.replace("[", "{").replace("]", "}") for src in GOOD_PY_LISTS],
    *[src.replace("[", "{").replace("]", "}") for src in PY_LISTS],
    "{a, b=c}",
    "{x=1, y=2}",
    "{{x=1,2,}, {3,y=4}}",
]


NON_JS_LISTS = ["[[]", "x", "]["]
NON_JSON_LISTS = JS_LISTS[len(JSON_LISTS) :] + NON_JS_LISTS
NON_PY_LISTS = JS_LISTS[len(PY_LISTS) :] + NON_JS_LISTS
NON_LISP_LISTS = JSON_LISTS + JS_LISTS
NON_LUA_LISTS = [src.replace("[", "{").replace("]", "}") for src in NON_PY_LISTS]


def check_valid(src: str, lang: str):
    try:
        listas.grammar(lang).parse(src)
    except LarkError as error:
        print(error)
        raise AssertionError(f"Entrada esperada como válida não foi aceita: {src}")


def check_invalid(src: str, lang: str):
    if listas.validate(src, lang):
        raise AssertionError(f"Entrada esperada como inválida foi aceita: {src}")


@pytest.mark.parametrize("src", JSON_LISTS + GOOD_LISTS)
def test_json_list_valid(src: str):
    check_valid(src, "json")


@pytest.mark.parametrize("src", NON_JSON_LISTS)
def test_json_list_invalid(src: str):
    check_invalid(src, "json")


@pytest.mark.parametrize("src", PY_LISTS + GOOD_LISTS + GOOD_PY_LISTS)
def test_py_list_valid(src: str):
    check_valid(src, "py")


@pytest.mark.parametrize("src", NON_PY_LISTS)
def test_py_list_invalid(src: str):
    check_invalid(src, "py")


@pytest.mark.parametrize("src", JS_LISTS + GOOD_LISTS + GOOD_PY_LISTS + GOOD_JS_LISTS)
def test_js_list_valid(src: str):
    check_valid(src, "js")


@pytest.mark.parametrize("src", NON_JS_LISTS)
def test_js_list_invalid(src: str):
    check_invalid(src, "js")


@pytest.mark.parametrize("src", LISP_LISTS)
def test_lisp_list_valid(src: str):
    check_valid(src, "lisp")


@pytest.mark.parametrize("src", NON_LISP_LISTS)
def test_lisp_list_invalid(src: str):
    check_invalid(src, "lisp")


@pytest.mark.parametrize("src", LUA_LISTS)
def test_lua_list_valid(src: str):
    check_valid(src, "lua")


@pytest.mark.parametrize("src", NON_LUA_LISTS)
def test_lua_list_invalid(src: str):
    check_invalid(src, "lua")
