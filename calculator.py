TAXAS_ANUAIS = {
    "selic": {"nome": "Selic", "taxa": 0.1050},
    "cdi": {"nome": "CDI", "taxa": 0.1040},
    "ipca": {"nome": "IPCA", "taxa": 0.0450},
    "poupanca": {"nome": "Poupanca", "taxa": 0.0617},
    "personalizada": {"nome": "Personalizada", "taxa": 0.0000},
}


def calcular_taxa_mensal(taxa_anual):
    return (1 + taxa_anual) ** (1 / 12) - 1


def calcular_evolucao(valor_inicial, aporte_mensal, meses, taxa_mensal):
    montante = valor_inicial
    total_investido = valor_inicial
    total_juros = 0.0
    linhas = []

    for mes in range(1, meses + 1):
        juros_mes = montante * taxa_mensal
        montante += juros_mes + aporte_mensal
        total_investido += aporte_mensal
        total_juros += juros_mes

        linhas.append(
            {
                "mes": mes,
                "juros_mes": juros_mes,
                "total_investido": total_investido,
                "total_juros": total_juros,
                "montante": montante,
            }
        )

    return linhas


def formatar_dinheiro(valor):
    texto = f"R$ {valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_percentual(valor):
    return f"{valor * 100:.2f}%".replace(".", ",")
