# [[Calculadora de Juros Compostos]]

Este projeto é uma calculadora web de [[Juros Compostos]] feita com
[[Python]], [[PyScript]], [[HTML]] e [[CSS]]. A aplicação roda no navegador,
mas usa código Python para calcular a evolução de um investimento ao longo do
tempo.

O usuário informa:

- [[Valor inicial]]
- [[Aporte mensal]]
- [[Periodo em meses]]
- [[Taxa anual]]

Depois disso, o sistema calcula mês a mês:

- [[Juros do mes]]
- [[Total investido]]
- [[Total de juros]]
- [[Total acumulado]]

---

## [[Objetivo do Projeto]]

O objetivo é demonstrar, de forma prática, como usar [[Python no navegador]]
para resolver um problema financeiro simples: simular a evolução de um valor
investido com [[Juros Compostos]].

O projeto também serve como base para praticar:

- organização de código em módulos;
- testes unitários com [[pytest]];
- padronização de código com [[Ruff]];
- gerenciamento de ambiente com [[uv]];
- integração entre [[Python]], [[PyScript]] e [[Interface Web]].

---

## [[Como Executar o Projeto]]

Para testar no navegador, suba um servidor local na pasta do projeto:

```bash
python3 -m http.server 8000
```

Depois acesse:

```text
http://localhost:8000/
```

Se a porta `8000` estiver ocupada, use outra porta:

```bash
python3 -m http.server 8001
```

E acesse:

```text
http://localhost:8001/
```

---

## [[Importancia do uv]]

O [[uv]] é o gerenciador usado neste projeto para facilitar a vida de todos os
integrantes da equipe.

Ele ajuda porque:

- instala as dependências de forma rápida;
- usa o arquivo `uv.lock` para manter as mesmas versões para todos;
- evita o problema de "na minha máquina funciona";
- simplifica a execução de ferramentas como [[pytest]] e [[Ruff]];
- deixa o ambiente do projeto mais previsível.

Na prática, o `uv.lock` registra exatamente quais versões foram resolvidas para
o projeto. Assim, quando outra pessoa clona o repositório e usa `uv`, ela recebe
um ambiente muito parecido com o dos outros integrantes.

Comandos importantes:

```bash
uv sync
```

Instala as dependências do projeto.

```bash
uv run pytest
```

Roda os testes unitários.

```bash
uv run ruff check .
```

Verifica problemas de estilo e qualidade no código.

```bash
uv run ruff format .
```

Formata o código Python automaticamente.

---

## [[Estrutura do Projeto]]

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

### [[index.html]]

Arquivo principal da interface. Ele define:

- campos do formulário;
- botão de calcular;
- tabela de resultados;
- carregamento do [[PyScript]];
- conexão com `main.py`;
- uso do arquivo `pyscript.json`.

O trecho mais importante é:

```html
<script type="py" src="./main.py" config="./pyscript.json"></script>
```

Esse comando faz o navegador executar o Python usando [[PyScript]].

### [[style.css]]

Arquivo responsável pelo visual da aplicação. Ele define layout, cores,
espaçamentos, botões, tabela e aparência geral da calculadora.

### [[main.py]]

Arquivo responsável pela integração entre o Python e a página HTML.

Ele faz:

- leitura dos valores digitados nos inputs;
- validação de campos negativos ou inválidos;
- chamada das funções de cálculo;
- montagem dos cards de resumo;
- preenchimento da tabela de resultados;
- conexão do botão `Calcular` com a função Python.

Este arquivo depende do navegador, porque usa:

```python
from pyscript import document
```

Por isso, ele não é o melhor lugar para testes unitários puros.

### [[calculator.py]]

Arquivo com a lógica pura do projeto. Ele não depende de HTML, navegador ou
PyScript.

Ele contém:

- `TAXAS_ANUAIS`;
- `calcular_taxa_mensal`;
- `calcular_evolucao`;
- `formatar_dinheiro`;
- `formatar_percentual`.

Como esse arquivo é Python puro, ele pode ser testado facilmente com [[pytest]].

### [[pyscript.json]]

Arquivo de configuração do PyScript.

Ele informa ao navegador que `calculator.py` também precisa ser carregado:

```json
{
  "files": {
    "./calculator.py": "./calculator.py"
  }
}
```

Sem esse arquivo, o navegador pode mostrar erro como:

```text
ModuleNotFoundError: No module named 'calculator'
```

### [[pyproject.toml]]

Arquivo de configuração do projeto Python.

Ele declara:

- nome do projeto;
- versão;
- versão mínima do Python;
- dependências principais;
- dependências de desenvolvimento;
- configuração do [[Ruff]];
- configuração do [[pytest]].

### [[uv.lock]]

Arquivo gerado pelo [[uv]] com as versões exatas das dependências.

Ele deve ser versionado no Git para garantir que todos usem versões
compatíveis.

### [[tests/test_calculator.py]]

Arquivo com testes unitários da lógica de cálculo.

Ele testa:

- cálculo da taxa mensal equivalente;
- evolução mês a mês;
- total investido;
- total de juros;
- montante final;
- formatação de dinheiro;
- formatação de percentual;
- comportamento com zero meses.

---

## [[Como o Codigo Funciona]]

### [[Taxas anuais]]

No arquivo `calculator.py`, existe um dicionário com taxas fixas:

```python
TAXAS_ANUAIS = {
    "selic": {"nome": "Selic", "taxa": 0.1050},
    "cdi": {"nome": "CDI", "taxa": 0.1040},
    "ipca": {"nome": "IPCA", "taxa": 0.0450},
    "poupanca": {"nome": "Poupanca", "taxa": 0.0617},
}
```

Cada taxa possui:

- um identificador, como `selic`;
- um nome exibido para o usuário;
- uma taxa anual em formato decimal.

Exemplo:

```text
0.1050 = 10,50% ao ano
```

### [[Taxa mensal equivalente]]

A função `calcular_taxa_mensal` transforma uma taxa anual em taxa mensal:

```python
def calcular_taxa_mensal(taxa_anual):
    return (1 + taxa_anual) ** (1 / 12) - 1
```

Isso é importante porque o cálculo da simulação acontece mês a mês.

### [[Evolucao do investimento]]

A função `calcular_evolucao` calcula a simulação mensal:

```python
def calcular_evolucao(valor_inicial, aporte_mensal, meses, taxa_mensal):
```

Ela começa com:

- `montante = valor_inicial`;
- `total_investido = valor_inicial`;
- `total_juros = 0.0`.

Para cada mês:

1. calcula os juros do mês;
2. soma os juros ao montante;
3. adiciona o aporte mensal;
4. atualiza o total investido;
5. atualiza o total de juros;
6. salva uma linha para exibir na tabela.

Exemplo simplificado:

```python
juros_mes = montante * taxa_mensal
montante += juros_mes + aporte_mensal
```

### [[Formatacao de valores]]

A função `formatar_dinheiro` transforma números em moeda brasileira:

```text
1234.5 -> R$ 1.234,50
```

A função `formatar_percentual` transforma valores decimais em porcentagem:

```text
0.105 -> 10,50%
```

### [[Fluxo da aplicacao]]

O fluxo geral é:

1. O usuário abre `index.html`.
2. O [[PyScript]] carrega `main.py`.
3. O `pyscript.json` garante que `calculator.py` também seja carregado.
4. O usuário preenche os campos.
5. O usuário clica em `Calcular`.
6. `main.py` lê os valores da página.
7. `main.py` chama as funções de `calculator.py`.
8. A página exibe resumo e tabela com a evolução do investimento.

---

## [[Testes com pytest]]

Os testes garantem que a lógica financeira continue funcionando mesmo quando o
código for alterado.

Para rodar:

```bash
uv run pytest
```

Resultado esperado:

```text
9 passed
```

Os testes ficam focados em `calculator.py`, porque ele não depende do navegador.
Isso deixa os testes mais rápidos, simples e confiáveis.

---

## [[Ruff]]

O [[Ruff]] é usado para manter o código Python organizado e padronizado.

Ele serve para:

- encontrar erros simples;
- avisar sobre imports não usados;
- identificar problemas de estilo;
- formatar o código automaticamente;
- manter um padrão entre todos os integrantes.

Comando para verificar:

```bash
uv run ruff check .
```

Comando para formatar:

```bash
uv run ruff format .
```

---

## [[Comandos Uteis]]

Instalar dependências:

```bash
uv sync
```

Rodar servidor local:

```bash
python3 -m http.server 8000
```

Rodar testes:

```bash
uv run pytest
```

Verificar qualidade:

```bash
uv run ruff check .
```

Formatar código:

```bash
uv run ruff format .
```

---

## [[Resumo Final]]

Este projeto combina [[Interface Web]] com [[Python no navegador]] para criar
uma calculadora de [[Juros Compostos]]. A lógica principal fica isolada em
`calculator.py`, a integração com a página fica em `main.py`, e os testes ficam
em `tests/test_calculator.py`.

O [[uv]] facilita a colaboração porque padroniza instalação, execução e versões
das dependências. O [[pytest]] protege a lógica do projeto com testes
automatizados, e o [[Ruff]] mantém o código limpo e consistente.
