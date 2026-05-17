# Calculadora de Juros Compostos

Aplicação web feita com Python, PyScript, HTML e CSS para
simular a evolução de um investimento com Juros Compostos.

O usuário informa Valor inicial, Aporte mensal, Periodo em meses e
Taxa anual. A aplicação calcula Juros do mes, Total investido,
Total de juros e Total acumulado.


## Resumo

Este projeto usa PyScript para executar Python no navegador. A interface
fica em `index.html`, a integração com a página fica em `main.py`, a regra de
negócio fica em `calculator.py`, e a qualidade é garantida com pytest,
Ruff e uv.


---

## Como rodar

Instale as dependências:

```bash
uv sync
```

Suba o servidor local:

```bash
python3 -m http.server 8000
```

Acesse no navegador:

```text
http://localhost:8000/
```

Se a porta `8000` estiver ocupada:

```bash
python3 -m http.server 8001
```

---

## Estrutura

```text
.
├── index.html
├── style.css
├── main.py
├── calculator.py
├── pyscript.json
├── pyproject.toml
├── uv.lock
└── tests/
    └── test_calculator.py
```

- index.html: define a interface e carrega o PyScript.
- style.css: define o visual da calculadora.
- main.py: conecta a página HTML com o código Python.
- calculator.py: contém a lógica pura de cálculo e formatação.
- pyscript.json: informa ao PyScript que `calculator.py` deve ser carregado.
- pyproject.toml: configura dependências, Ruff e pytest.
- uv.lock: fixa as versões das dependências.
- tests/test_calculator.py: testa a lógica de `calculator.py`.

---

## Como funciona

O fluxo da aplicação é:

1. O navegador abre `index.html`.
2. O PyScript executa `main.py`.
3. O `pyscript.json` carrega `calculator.py` no ambiente do navegador.
4. O usuário preenche os campos e clica em `Calcular`.
5. `main.py` lê os valores da página.
6. `calculator.py` calcula a evolução do investimento.
7. `main.py` renderiza o resumo e a tabela.

As taxas ficam em `calculator.py`:

```python
TAXAS_ANUAIS = {
    "selic": {"nome": "Selic", "taxa": 0.1050},
    "cdi": {"nome": "CDI", "taxa": 0.1040},
    "ipca": {"nome": "IPCA", "taxa": 0.0450},
    "poupanca": {"nome": "Poupanca", "taxa": 0.0617},
}
```

A taxa anual é convertida para taxa mensal equivalente:

```python
(1 + taxa_anual) ** (1 / 12) - 1
```

Depois, para cada mês, o projeto calcula juros, aporte, total investido e total
acumulado.

---

## uv

O uv facilita o trabalho em equipe porque instala dependências rapidamente e
usa o `uv.lock` para manter as mesmas versões entre todos os integrantes.

Isso reduz problemas como:

```text
na minha máquina funciona
```

Comandos principais:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format .
```

---

## Testes e qualidade

Rodar testes:

```bash
uv run pytest
```

Rodar lint:

```bash
uv run ruff check .
```

Formatar código:

```bash
uv run ruff format .
```

Os testes focam em `calculator.py`, porque ele é Python puro e não depende do
navegador.

---

