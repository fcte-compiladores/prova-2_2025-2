import pytest

from lox.lox import parse


def test_parse_array_vazia():
    parse("[];")


def test_parse_array_simples():
    parse('["a", "b", "c"];')


def test_parse_array_aninhada():
    parse('["a", ["b", ["c"]]];')


def test_recusa_array_com_vírgula_no_final():
    with pytest.raises(Exception):
        parse('["a", "b", "c",];')


def test_recusa_array_sem_vigulas():
    with pytest.raises(Exception):
        parse('["a", "b", "c",];')


def test_recusa_formatos_inválidos_de_datas():
    with pytest.raises(Exception):
        parse("'2025-1-1;")
    with pytest.raises(Exception):
        parse("'2025-1-010;")


def test_recusa_datas_com_digitos_invalidos():
    with pytest.raises(Exception):
        parse("'2025-01-३०;")


def test_aceita_atribuicao_dentro_da_array():
    parse('[x = "a", "b", "c"];')


def test_aceita_operacao_matematica_no_elemento():
    parse('["a" + "b" == "ab", "c"];')


def test_aceita_datas():
    parse("'2025-11-27;")


def test_aceita_arrays_com_datas():
    parse("['2025-11-27, '2024-01-01];")


def test_aceita_subtracao_de_datas():
    parse("'2025-11-27 - '2024-01-01;")
