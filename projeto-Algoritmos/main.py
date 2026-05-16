from pyodide.ffi import create_proxy
from pyscript import document


TAXAS_ANUAIS = {
    "selic": {"nome": "Selic", "taxa": 0.1050},
    "cdi": {"nome": "CDI", "taxa": 0.1040},
    "ipca": {"nome": "IPCA", "taxa": 0.0450},
    "poupanca": {"nome": "Poupanca", "taxa": 0.0617},
}


def obter_float(element_id):
    valor = document.getElementById(element_id).value
    if not valor:
        return 0.0
    return float(valor)


def obter_inteiro(element_id):
    valor = document.getElementById(element_id).value
    if not valor:
        return 0
    return int(float(valor))


def formatar_dinheiro(valor):
    texto = f"R$ {valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_percentual(valor):
    return f"{valor * 100:.2f}%".replace(".", ",")


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


def criar_card(titulo, valor):
    return f"""
        <article class="summary-card">
            <span>{titulo}</span>
            <strong>{valor}</strong>
        </article>
    """


def renderizar_resumo(taxa_info, taxa_mensal, valor_final, total_investido, total_juros):
    summary = document.getElementById("summary")
    summary.innerHTML = (
        criar_card("Taxa escolhida", taxa_info["nome"])
        + criar_card("Taxa anual", formatar_percentual(taxa_info["taxa"]))
        + criar_card("Taxa mensal equivalente", formatar_percentual(taxa_mensal))
        + criar_card("Valor final", formatar_dinheiro(valor_final))
        + criar_card("Total investido", formatar_dinheiro(total_investido))
        + criar_card("Total em juros", formatar_dinheiro(total_juros))
    )


def renderizar_tabela(linhas):
    table_body = document.getElementById("result-table")
    conteudo = ""

    for linha in linhas:
        conteudo += f"""
            <tr>
                <td>{linha["mes"]}</td>
                <td>{formatar_dinheiro(linha["juros_mes"])}</td>
                <td>{formatar_dinheiro(linha["total_investido"])}</td>
                <td>{formatar_dinheiro(linha["total_juros"])}</td>
                <td>{formatar_dinheiro(linha["montante"])}</td>
            </tr>
        """

    table_body.innerHTML = conteudo


def mostrar_erro(mensagem):
    document.getElementById("error-message").innerText = mensagem


def limpar_erro():
    mostrar_erro("")


def calcular(event):
    event.preventDefault()
    limpar_erro()

    try:
        valor_inicial = obter_float("initial-value")
        aporte_mensal = obter_float("monthly-contribution")
        meses = obter_inteiro("months")
        taxa_id = document.getElementById("rate-type").value

        if valor_inicial < 0 or aporte_mensal < 0:
            mostrar_erro("Os valores nao podem ser negativos.")
            return

        if meses <= 0:
            mostrar_erro("Informe um periodo maior que zero.")
            return

        taxa_info = TAXAS_ANUAIS[taxa_id]
        taxa_mensal = (1 + taxa_info["taxa"]) ** (1 / 12) - 1
        linhas = calcular_evolucao(valor_inicial, aporte_mensal, meses, taxa_mensal)

        ultima_linha = linhas[-1]
        renderizar_resumo(
            taxa_info,
            taxa_mensal,
            ultima_linha["montante"],
            ultima_linha["total_investido"],
            ultima_linha["total_juros"],
        )
        renderizar_tabela(linhas)
    except ValueError:
        mostrar_erro("Preencha os campos com numeros validos.")


form = document.getElementById("calculator-form")
form.addEventListener("submit", create_proxy(calcular))
