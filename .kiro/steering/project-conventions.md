---
inclusion: always
---

# Convenções do Projeto — mapa-pegada-digital

Este arquivo é carregado automaticamente em toda sessão Kiro.
Ele define padrões, restrições e decisões arquiteturais do projeto.

---

## Stack e ambiente

- Linguagem: **Python 3.11+** (testado até 3.14)
- Empacotamento: `setuptools` via `pyproject.toml`; instalar com `pip install -e ".[dev]"`
- Testes: **pytest ≥ 8**; rodar com `pytest -q`
- Lint: **ruff ≥ 0.6**, linha máx. 100 chars; rodar com `ruff check .`
- Sem Docker, sem Node, sem compiladores nativos
- Biblioteca padrão Python preferida a dependências externas

## Dependências de produção aprovadas

| Pacote | Uso |
|---|---|
| `reportlab >=4.2,<5` | Geração de PDF |
| `python-dotenv >=1.0,<2` | Leitura de `.env` |
| `notion-client >=3.1,<4` | Sync com Notion (extra opcional `[notion]`) |

Não introduzir novas dependências sem atualizar `pyproject.toml` e documentar aqui.

## Convenções de código

- Módulos ficam em `src/pegada/`; testes em `tests/`
- Imports absolutos dentro do pacote (`from pegada.models import Evidence`)
- `from __future__ import annotations` no topo de todos os módulos
- Dataclasses com `slots=True` para modelos de dados
- Funções puras preferidas a classes quando não há estado
- Sem `print` em bibliotecas; apenas na CLI (`cli.py`)

## Modelo de dados central

`Evidence` (em `models.py`) é o único tipo de dado trafegado entre camadas.
Campos obrigatórios: `title`, `url`, `source`.
Fingerprint = SHA-256 de `url.lower() | title.lower() | category`.
`identity_status` inicia sempre como `"pending"`.

## Regras de coleta (não negociáveis)

1. Não contornar autenticação, CAPTCHA ou bloqueios.
2. Respeitar `robots.txt` e intervalo mínimo de 1s entre requisições.
3. Resultados automáticos são candidatos — `identity_status = "pending"`.
4. Apenas dados publicamente acessíveis.

## Banco de dados

- SQLite único em `data/pegada.sqlite3` (configurável via `PEGADA_DB`)
- Deduplicação por `fingerprint UNIQUE` — upsert, nunca insert cego
- Tabela `runs` para trilha de auditoria de execuções de coletores
- Não usar ORM; SQL direto com `sqlite3` da stdlib

## Notion Sync

- Operação explícita — nunca automática ou implícita
- Sempre validar esquema remoto antes de gravar
- `--dry-run` obrigatório antes de qualquer envio real em novo ambiente
- Idempotente: usar `Fingerprint` para criar ou atualizar, nunca duplicar

## Saídas

- Diretório `output/` (configurável via `PEGADA_OUTPUT`)
- Arquivos: `evidencias.json`, `evidencias.csv`, `mapa_pegada_digital.md`, PDF
- `output/` está no `.gitignore` (exceto `.gitkeep`)

## Fluxo de contribuição (CI)

- Branch `main` protegida: PR obrigatório, check `test` deve passar
- Force push e deleção de branch bloqueados
- Criar branch: `git switch -c feat/<nome>` ou `fix/<nome>`
- CI: `pytest` + `ruff check .` em `ubuntu-latest` / Python 3.11

## Spec-Driven Development

Todo trabalho novo deve ter spec antes de código:
1. `requirements.md` — user stories e critérios de aceitação
2. `design.md` — arquitetura, componentes, interfaces, propriedades de correção
3. `tasks.md` — lista de tarefas atômicas e implementáveis

Specs ficam em `.kiro/specs/{feature-name}/`.
Não modificar código sem spec correspondente aprovada.
