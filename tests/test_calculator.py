import pytest

from calculator import (
    calcular_evolucao,
    calcular_taxa_mensal,
    formatar_dinheiro,
    formatar_percentual,
)


def test_calcular_taxa_mensal_equivalente():
    taxa_mensal = calcular_taxa_mensal(0.12)

    assert taxa_mensal == pytest.approx(0.009488792934583046)


def test_calcular_evolucao_mes_a_mes():
    linhas = calcular_evolucao(
        valor_inicial=1000.0,
        aporte_mensal=100.0,
        meses=2,
        taxa_mensal=0.01,
    )

    assert linhas == [
        {
            "mes": 1,
            "juros_mes": pytest.approx(10.0),
            "total_investido": pytest.approx(1100.0),
            "total_juros": pytest.approx(10.0),
            "montante": pytest.approx(1110.0),
        },
        {
            "mes": 2,
            "juros_mes": pytest.approx(11.1),
            "total_investido": pytest.approx(1200.0),
            "total_juros": pytest.approx(21.1),
            "montante": pytest.approx(1221.1),
        },
    ]


def test_calcular_evolucao_sem_meses_retorna_lista_vazia():
    linhas = calcular_evolucao(
        valor_inicial=1000.0,
        aporte_mensal=100.0,
        meses=0,
        taxa_mensal=0.01,
    )

    assert linhas == []


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0, "R$ 0,00"),
        (1234.5, "R$ 1.234,50"),
        (1000000.99, "R$ 1.000.000,99"),
    ],
)
def test_formatar_dinheiro(valor, esperado):
    assert formatar_dinheiro(valor) == esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0, "0,00%"),
        (0.105, "10,50%"),
        (0.009488792934583046, "0,95%"),
    ],
)
def test_formatar_percentual(valor, esperado):
    assert formatar_percentual(valor) == esperado
