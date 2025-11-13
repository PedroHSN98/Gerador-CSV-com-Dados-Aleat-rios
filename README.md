# Gerador de CSV — Dados Aleatórios (pt-BR) / CSV Generator — Random Data (EN)

Este repositório inclui o script `gerador_csv.py` e um README bilingue. Existem versões/descrições em Português (pt-BR) e Inglês (EN) neste mesmo arquivo.

---

## Português (pt-BR)

Um gerador interativo de arquivos CSV com dados fictícios em português do Brasil. Útil para testes, demonstrações, demos de BI, população de bases de teste e ensino.

### O que este projeto faz

- Gera arquivos CSV com colunas definidas pelo usuário.
- Para cada coluna, você escolhe o tipo de dado (nome, e-mail, CPF falso, data, número, etc.) e o nome da coluna.
- Alguns tipos permitem configurações (intervalos, quantidade de casas decimais, opções de lista, intervalo de anos para datas, etc.).
- Gera N linhas e salva em um arquivo CSV UTF-8 separado por vírgula.
- Usa apenas a biblioteca padrão do Python. Se o pacote `Faker` estiver instalado, ele será usado para enriquecer os nomes/endereços (locale `pt_BR`).

### Arquivos no repositório

- `gerador_csv.py` — Script principal (interativo).
- `4_colunas.csv`, `gerador_teste.csv` — Exemplo(s) de saída (se presentes no repositório).

### Requisitos

- Python 3.10 ou superior (o código usa sintaxe de tipagem introduzida no Python 3.10).
- Opcional: `Faker` (para dados mais realistas, locale `pt_BR`).

Para instalar o Faker (opcional):

```powershell
pip install Faker
```

Recomendo utilizar um ambiente virtual (venv) para não poluir o Python do sistema.

### Passo a passo (Windows PowerShell)

1. Abra o PowerShell na pasta do projeto (onde está `gerador_csv.py`).

2. (Opcional, recomendado) Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
# Se receber erro de execução, execute (como administrador ou no seu perfil):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Atualize o pip e instale o Faker se desejar dados mais realistas:

```powershell
python -m pip install --upgrade pip
pip install Faker
```

4. Execute o gerador (modo interativo):

```powershell
python .\\gerador_csv.py
```

Siga as perguntas interativas: escolha quantas colunas, tipos, nomes, configurações específicas (ex.: min/max para números), quantas linhas gerar e nome do arquivo de saída.

Dica: para aceitar o valor padrão em qualquer prompt, pressione Enter.

### Observações importantes

- Encoding / Excel: O arquivo é salvo em UTF-8 com vírgula como separador. Dependendo da sua versão do Excel e das configurações regionais, o Excel no Windows pode esperar ponto-e-vírgula como separador. Se o Excel não abrir corretamente, importe o arquivo no Excel usando a opção "Importar texto/CSV" e selecione UTF-8 e delimitador vírgula.

- Python versão: O script usa anotações de tipo com `|` (p.ex. `int | None`) — requer Python 3.10+. Em Python mais antigo esse código causará erro de sintaxe.

- Execução não interativa: o script é interativo e não possui argumentos de linha de comando para gerar automaticamente. Para automatizar, você pode:
  - Usar redirecionamento de entrada com um arquivo contendo respostas, ou
  - Adaptar o script para aceitar argumentos CLI (por exemplo usando `argparse`).

### Tipos de coluna suportados (resumo)

Alguns tipos disponíveis: Nome completo, Nome, Sobrenome, E-mail, Telefone, CPF, Endereço, Cidade, Estado (UF), CEP, Data, Data e Hora, Inteiro, Decimal (float), Booleano, UUID, Empresa, Cargo, URL, Texto curto (lorem), Lista de opções (picklist), Preço.

Se o `Faker` estiver instalado, geradores como nomes, e-mails, endereços e empresas ficam mais realistas (locale `pt_BR`).

---

## English (EN)

An interactive CSV generator that creates sample datasets with realistic-looking values (Portuguese/Brazilian by default). Useful for testing, demos, BI samples, QA and teaching.

### What this project does

- Generates CSV files with user-defined columns.
- For each column you choose the data type (name, email, fake CPF, date, number, etc.) and the column header.
- Some types have configurable parameters (ranges, decimal precision, picklist options, year ranges for dates, etc.).
- Produces N rows and saves to a UTF-8 CSV file using comma as delimiter.
- Uses only Python standard library. If the `Faker` package is installed it will be used to produce richer data (locale `pt_BR`).

### Files in the repository

- `gerador_csv.py` — Main interactive script.
- `4_colunas.csv`, `gerador_teste.csv` — Example output files (if present).

### Requirements

- Python 3.10 or newer (script uses modern type annotation syntax).
- Optional: `Faker` package (for more realistic names/addresses).

To install Faker (optional):

```powershell
pip install Faker
```

Using a virtual environment is recommended.

### Quick start (Windows PowerShell)

1. Open PowerShell in the project folder (where `gerador_csv.py` is).

2. (Optional, recommended) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
# If you get an execution policy error, run (as admin or set for current user):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Upgrade pip and install Faker if desired:

```powershell
python -m pip install --upgrade pip
pip install Faker
```

4. Run the generator (interactive):

```powershell
python .\\gerador_csv.py
```

Follow the interactive prompts to select number of columns, types, names, specific configs (e.g. min/max for numbers), number of rows and output filename.

Tip: press Enter to accept the default value on any prompt.

### Notes

- Encoding / Excel: The file is saved as UTF-8 with comma delimiter. Excel on Windows may expect semicolon depending on regional settings — if data looks wrong, import the CSV via Excel's "From Text/CSV" wizard and choose UTF-8 and comma delimiter.

- Python version: the script uses type annotations like `int | None`, which require Python 3.10+. Using older Python will raise a syntax error.

- Non-interactive usage: the script is interactive and does not yet accept CLI arguments. To automate, you can either redirect input from a prepared file or modify the script to accept arguments using `argparse`.

### Supported column types (summary)

Examples: Full name, First name, Last name, Email, Phone, CPF (fake), Address, City, State (UF), CEP, Date, Datetime, Integer, Float, Boolean, UUID, Company, Job, URL, Short text (lorem), Picklist, Price.

If `Faker` is installed, generators for names, emails, addresses and companies will be more realistic (pt_BR locale).

---

## Notes about versions / localization

- This repository and README provide information in both Portuguese (pt-BR) and English (EN).
- The script `gerador_csv.py` prints prompts in Portuguese but is usable by English speakers — responses are simple (numbers, text, S/N for yes/no). If you want, I can add an English-mode to the script so prompts are shown in English when requested.

---

If you want, I can:

- Add a `requirements.txt` listing `Faker`.
- Implement a non-interactive mode using `argparse`.
- Add an English-mode to the script (switch language at start).

Tell me which one you'd like next and I will implement it.
