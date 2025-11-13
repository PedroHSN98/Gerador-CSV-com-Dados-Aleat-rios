#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador Interativo de CSV com Dados Aleatórios (pt-BR)
------------------------------------------------------
- Permite escolher quantas colunas o CSV terá
- Para cada coluna, você escolhe o TIPO de dado e o NOME da coluna
- Alguns tipos têm configurações personalizadas (ex.: intervalos, opções, etc.)
- Ao final, você escolhe quantas linhas (registros) serão geradas
- Saída em UTF-8, separador vírgula

Requisitos:
- Somente biblioteca padrão do Python.
- Opcional: Se você tiver o pacote 'Faker' instalado, ele será usado para enriquecer os dados (locale pt_BR).
  Para instalar: pip install Faker

Uso:
    python gerador_csv.py
"""

from __future__ import annotations

import csv
import os
import random
import sys
import uuid as uuidlib
from datetime import datetime, timedelta

# Tentativa opcional de usar Faker (se existir).
_FAKE = None
try:
    from faker import Faker  # type: ignore
    _FAKE = Faker('pt_BR')
except Exception:
    _FAKE = None

# ------------------------- Utilitários -------------------------

def prompt_int(msg: str, min_val: int | None = None, max_val: int | None = None, default: int | None = None) -> int:
    while True:
        raw = input(f"{msg}" + (f" [padrão: {default}]" if default is not None else "") + ": ").strip()
        if not raw and default is not None:
            return default
        if not raw.isdigit():
            print("⚠️  Por favor, digite um número inteiro válido.")
            continue
        val = int(raw)
        if min_val is not None and val < min_val:
            print(f"⚠️  Valor mínimo: {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"⚠️  Valor máximo: {max_val}.")
            continue
        return val

def prompt_float(msg: str, default: float | None = None) -> float:
    while True:
        raw = input(f"{msg}" + (f" [padrão: {default}]" if default is not None else "") + ": ").strip().replace(",", ".")
        if not raw and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print("⚠️  Por favor, digite um número (pode usar vírgula).")

def prompt_str(msg: str, default: str | None = None) -> str:
    raw = input(f"{msg}" + (f" [padrão: {default}]" if default is not None else "") + ": ").strip()
    if not raw and default is not None:
        return default
    return raw

def prompt_yes_no(msg: str, default_yes: bool = True) -> bool:
    default = "S" if default_yes else "N"
    while True:
        raw = input(f"{msg} (S/N) [padrão: {default}]: ").strip().lower()
        if not raw:
            return default_yes
        if raw in ("s", "sim", "y", "yes"):
            return True
        if raw in ("n", "nao", "não", "no"):
            return False
        print("⚠️  Responda com S/N.")

# --------------------- Fallbacks (sem Faker) -------------------

FIRST_NAMES = ["Gabriel", "Maria", "Ana", "João", "Pedro", "Lucas", "Julia", "Mariana", "Rafael", "Beatriz"]
LAST_NAMES  = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima", "Carvalho", "Gomes", "Almeida", "Ferreira"]
CITIES      = ["São Paulo", "Rio de Janeiro", "Cuiabá", "Belo Horizonte", "Curitiba", "Salvador", "Fortaleza", "Recife"]
STATES      = ["SP", "RJ", "MT", "MG", "PR", "BA", "CE", "PE"]
COMPANIES   = ["InovaTech", "Alpha Sistemas", "Data+Brasil", "Azul Digital", "TecnoSul", "Norte Cloud"]
JOBS        = ["Analista de Sistemas", "Engenheiro de Software", "Suporte Técnico", "Cientista de Dados", "DevOps"]
DOMAINS     = ["exemplo.com", "empresa.com.br", "corp.br", "mail.com"]

def rand_first_name():
    if _FAKE:
        return _FAKE.first_name()
    return random.choice(FIRST_NAMES)

def rand_last_name():
    if _FAKE:
        return _FAKE.last_name()
    return random.choice(LAST_NAMES)

def rand_full_name():
    if _FAKE:
        return _FAKE.name()
    return f"{rand_first_name()} {rand_last_name()}"

def rand_email():
    if _FAKE:
        return _FAKE.free_email()
    fn = rand_first_name().lower()
    ln = rand_last_name().lower()
    dom = random.choice(DOMAINS)
    return f"{fn}.{ln}@{dom}"

def rand_phone():
    # Formato brasileiro típico: (DD) 9XXXX-XXXX
    ddd = random.randint(11, 99)
    prefixo = random.randint(90000, 99999)
    sufixo = random.randint(0000, 9999)
    return f"({ddd}) {prefixo:05d}-{sufixo:04d}"

def rand_company():
    if _FAKE:
        return _FAKE.company()
    return random.choice(COMPANIES)

def rand_job():
    if _FAKE:
        return _FAKE.job()
    return random.choice(JOBS)

def rand_city():
    if _FAKE:
        return _FAKE.city()
    return random.choice(CITIES)

def rand_state():
    if _FAKE:
        # Nem sempre retorna sigla; mas ok.
        return _FAKE.estado_sigla() if hasattr(_FAKE, "estado_sigla") else random.choice(STATES)
    return random.choice(STATES)

def rand_address():
    if _FAKE:
        return _FAKE.address().replace("\n", ", ")
    # Fallback simples
    num = random.randint(1, 9999)
    return f"Rua {rand_last_name()}, {num}, {rand_city()} - {rand_state()}"

def rand_cep(formatado=True):
    # CEP: 8 dígitos; formato comum 00000-000
    d = [random.randint(0,9) for _ in range(8)]
    if formatado:
        return f"{d[0]}{d[1]}{d[2]}{d[3]}{d[4]}-{d[5]}{d[6]}{d[7]}"
    return "".join(str(x) for x in d)

# --------------------- Geradores numéricos ---------------------

def rand_int(min_val: int = 0, max_val: int = 100) -> int:
    return random.randint(min_val, max_val)

def rand_float(min_val: float = 0.0, max_val: float = 100.0, decimals: int = 2) -> float:
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    val = random.random() * (max_val - min_val) + min_val
    return round(val, decimals)

def rand_bool() -> bool:
    return random.choice([True, False])

def rand_uuid() -> str:
    return str(uuidlib.uuid4())

# --------------------- Datas e Horários ------------------------

def rand_date(year_start: int = 2010, year_end: int = datetime.now().year) -> str:
    y = random.randint(year_start, year_end)
    # garantir meses/dias válidos de forma simples
    start = datetime(y, 1, 1)
    end = datetime(y, 12, 31)
    delta = end - start
    rd = start + timedelta(days=random.randint(0, delta.days))
    return rd.strftime("%Y-%m-%d")

def rand_datetime(year_start: int = 2010, year_end: int = datetime.now().year) -> str:
    y = random.randint(year_start, year_end)
    start = datetime(y, 1, 1, 0, 0, 0)
    end = datetime(y, 12, 31, 23, 59, 59)
    total_seconds = int((end - start).total_seconds())
    offset = random.randint(0, total_seconds)
    dt = start + timedelta(seconds=offset)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# --------------------- CPF (com dígitos) -----------------------

def _cpf_dv(digs: list[int]) -> int:
    # Calcula dígito verificador (módulo 11)
    peso = list(range(len(digs) + 1, 1, -1))
    soma = sum(d * p for d, p in zip(digs, peso))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto

def rand_cpf(formatado: bool = True) -> str:
    base = [random.randint(0, 9) for _ in range(9)]
    dv1 = _cpf_dv(base)
    dv2 = _cpf_dv(base + [dv1])
    nums = base + [dv1, dv2]
    if formatado:
        return f"{nums[0]}{nums[1]}{nums[2]}.{nums[3]}{nums[4]}{nums[5]}.{nums[6]}{nums[7]}{nums[8]}-{nums[9]}{nums[10]}"
    return "".join(str(n) for n in nums)

# --------------------- Texto / URL -----------------------------

LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore "
    "et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip "
    "ex ea commodo consequat duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
    "fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt "
    "mollit anim id est laborum"
).split()

def rand_sentence(min_words: int = 4, max_words: int = 12) -> str:
    n = random.randint(min_words, max_words)
    words = random.choices(LOREM_WORDS, k=n)
    s = " ".join(words)
    return s.capitalize() + "."

def rand_url():
    if _FAKE:
        return _FAKE.url()
    # Fallback simples
    host = random.choice(["site", "app", "portal", "blog"])
    tld = random.choice(["com", "com.br", "net", "org"])
    path = random.choice(["home", "produto", "contato", "sobre"])
    return f"https://{host}{random.randint(1,999)}.{tld}/{path}"

# ---------------------- Tipos de Coluna ------------------------

class ColumnType:
    def __init__(self, code: str, label: str, needs_config=False):
        self.code = code
        self.label = label
        self.needs_config = needs_config

    def __repr__(self):
        return f"<{self.code}: {self.label}>"

COLUMN_TYPES = [
    ColumnType("full_name", "Nome completo"),
    ColumnType("first_name", "Nome"),
    ColumnType("last_name", "Sobrenome"),
    ColumnType("email", "E-mail"),
    ColumnType("phone", "Telefone (BR)"),
    ColumnType("cpf", "CPF (falso)"),
    ColumnType("address", "Endereço completo"),
    ColumnType("city", "Cidade"),
    ColumnType("state", "Estado (UF)"),
    ColumnType("cep", "CEP (falso)"),
    ColumnType("date", "Data (YYYY-MM-DD)", needs_config=True),
    ColumnType("datetime", "Data e Hora (YYYY-MM-DD HH:MM:SS)", needs_config=True),
    ColumnType("int", "Número inteiro", needs_config=True),
    ColumnType("float", "Número decimal", needs_config=True),
    ColumnType("bool", "Booleano"),
    ColumnType("uuid", "UUID v4"),
    ColumnType("company", "Empresa"),
    ColumnType("job", "Cargo (trabalho)"),
    ColumnType("url", "URL"),
    ColumnType("sentence", "Texto curto (lorem)"),
    ColumnType("picklist", "Lista de opções (categorias)", needs_config=True),
    ColumnType("price", "Preço monetário", needs_config=True),
]

def show_menu():
    print("\nTipos de coluna disponíveis:")
    for i, ct in enumerate(COLUMN_TYPES, start=1):
        print(f"  {i:2d}. {ct.label}  (código: {ct.code})")

def get_column_config(col_type_code: str) -> dict:
    cfg = {}
    if col_type_code == "int":
        cfg["min"] = prompt_int("  - Valor mínimo (inteiro)", default=0)
        cfg["max"] = prompt_int("  - Valor máximo (inteiro)", default=100)
        if cfg["min"] > cfg["max"]:
            cfg["min"], cfg["max"] = cfg["max"], cfg["min"]
    elif col_type_code == "float":
        cfg["min"] = prompt_float("  - Valor mínimo", default=0.0)
        cfg["max"] = prompt_float("  - Valor máximo", default=100.0)
        cfg["decimals"] = prompt_int("  - Casas decimais", min_val=0, max_val=10, default=2)
        if cfg["min"] > cfg["max"]:
            cfg["min"], cfg["max"] = cfg["max"], cfg["min"]
    elif col_type_code == "date":
        cfg["year_start"] = prompt_int("  - Ano inicial (ex.: 2015)", default=2015)
        cfg["year_end"]   = prompt_int("  - Ano final (ex.: 2025)", default=datetime.now().year)
        if cfg["year_start"] > cfg["year_end"]:
            cfg["year_start"], cfg["year_end"] = cfg["year_end"], cfg["year_start"]
    elif col_type_code == "datetime":
        cfg["year_start"] = prompt_int("  - Ano inicial (ex.: 2015)", default=2015)
        cfg["year_end"]   = prompt_int("  - Ano final (ex.: 2025)", default=datetime.now().year)
        if cfg["year_start"] > cfg["year_end"]:
            cfg["year_start"], cfg["year_end"] = cfg["year_end"], cfg["year_start"]
    elif col_type_code == "picklist":
        opts = prompt_str("  - Opções separadas por vírgula (ex.: Novo,Em andamento,Concluído)", default="A,B,C")
        cfg["options"] = [o.strip() for o in opts.split(",") if o.strip()]
    elif col_type_code == "price":
        cfg["min"] = prompt_float("  - Preço mínimo", default=10.0)
        cfg["max"] = prompt_float("  - Preço máximo", default=1000.0)
        cfg["decimals"] = prompt_int("  - Casas decimais", min_val=0, max_val=4, default=2)
        if cfg["min"] > cfg["max"]:
            cfg["min"], cfg["max"] = cfg["max"], cfg["min"]
    return cfg

def build_generator(col_type_code: str, cfg: dict):
    # Retorna uma função sem argumentos que gera o valor (string)
    if col_type_code == "full_name":
        return lambda: rand_full_name()
    if col_type_code == "first_name":
        return lambda: rand_first_name()
    if col_type_code == "last_name":
        return lambda: rand_last_name()
    if col_type_code == "email":
        return lambda: rand_email()
    if col_type_code == "phone":
        return lambda: rand_phone()
    if col_type_code == "cpf":
        return lambda: rand_cpf(formatado=True)
    if col_type_code == "address":
        return lambda: rand_address()
    if col_type_code == "city":
        return lambda: rand_city()
    if col_type_code == "state":
        return lambda: rand_state()
    if col_type_code == "cep":
        return lambda: rand_cep(formatado=True)
    if col_type_code == "date":
        ys, ye = cfg.get("year_start", 2015), cfg.get("year_end", datetime.now().year)
        return lambda: rand_date(ys, ye)
    if col_type_code == "datetime":
        ys, ye = cfg.get("year_start", 2015), cfg.get("year_end", datetime.now().year)
        return lambda: rand_datetime(ys, ye)
    if col_type_code == "int":
        mn, mx = cfg.get("min", 0), cfg.get("max", 100)
        return lambda: str(rand_int(mn, mx))
    if col_type_code == "float":
        mn, mx, dec = cfg.get("min", 0.0), cfg.get("max", 100.0), cfg.get("decimals", 2)
        return lambda: f"{rand_float(mn, mx, dec):.{dec}f}"
    if col_type_code == "bool":
        return lambda: "true" if rand_bool() else "false"
    if col_type_code == "uuid":
        return lambda: rand_uuid()
    if col_type_code == "company":
        return lambda: rand_company()
    if col_type_code == "job":
        return lambda: rand_job()
    if col_type_code == "url":
        return lambda: rand_url()
    if col_type_code == "sentence":
        return lambda: rand_sentence()
    if col_type_code == "picklist":
        options = cfg.get("options", ["A", "B", "C"])
        return lambda: random.choice(options)
    if col_type_code == "price":
        mn, mx, dec = cfg.get("min", 10.0), cfg.get("max", 1000.0), cfg.get("decimals", 2)
        return lambda: f"{rand_float(mn, mx, dec):.{dec}f}"
    # fallback: UUID
    return lambda: rand_uuid()

def main():
    print("=== GERADOR DE CSV — Dados Aleatórios (pt-BR) ===")
    # Semente opcional para reprodutibilidade
    if prompt_yes_no("Deseja fixar uma semente aleatória para repetir os mesmos dados no futuro?", default_yes=False):
        seed = prompt_int("  - Informe um número inteiro para a semente", default=42)
        random.seed(seed)
        if _FAKE:
            _FAKE.seed_instance(seed)

    num_cols = prompt_int("\nQuantas colunas terá o CSV?", min_val=1, max_val=200, default=5)
    columns = []  # lista de (header, generator)

    for i in range(1, num_cols + 1):
        print(f"\n— Configuração da coluna {i}/{num_cols}")
        show_menu()
        idx = prompt_int("  Escolha o tipo (digite o número da lista)", min_val=1, max_val=len(COLUMN_TYPES), default=1)
        col_type = COLUMN_TYPES[idx - 1]
        col_name = prompt_str("  Nome da coluna", default=col_type.label)

        cfg = {}
        if col_type.needs_config:
            print("  > Este tipo possui configurações:")
            cfg = get_column_config(col_type.code)

        gen_fn = build_generator(col_type.code, cfg)
        columns.append((col_name, gen_fn))

    num_rows = prompt_int("\nQuantas LINHAS deseja gerar?", min_val=1, max_val=10_000_000, default=1000)
    default_filename = "dados_aleatorios.csv"
    out_name = prompt_str("Nome do arquivo CSV de saída", default=default_filename)

    # Geração do CSV
    created = 0
    with open(out_name, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([h for (h, _) in columns])
        for _ in range(num_rows):
            row = [gen() for (_, gen) in columns]
            writer.writerow(row)
            created += 1

    size_mb = os.path.getsize(out_name) / (1024 * 1024)
    print(f"\n✅ Arquivo '{out_name}' gerado com sucesso!")
    print(f"   Linhas: {created:,} | Colunas: {len(columns)} | Tamanho aprox.: {size_mb:.2f} MB")
    print("   Dica: abra no Excel, LibreOffice Calc ou Power BI.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(1)
