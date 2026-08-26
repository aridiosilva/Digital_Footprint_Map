# BUILD.md — Guia de Construção e Desenvolvimento

Este documento descreve como instalar, testar, executar e manter o projeto
**mapa-pegada-digital** (`pegada`) em ambiente de desenvolvimento local.

---

## Pré-requisitos

| Ferramenta | Versão mínima | Observação |
|---|---|---|
| Python | 3.11 | Testado até 3.14. Recomendado usar `venv` isolado. |
| pip | qualquer recente | Atualizado como primeiro passo da instalação |
| Git | qualquer | Para controle de versão e CI |

Nenhuma ferramenta de build nativa (C compiler, Docker, Node, etc.) é necessária.

---

## Configuração inicial

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd Digital_Footprint_Map

# 2. Crie e ative o ambiente virtual
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 3. Instale o pacote em modo editável com dependências de desenvolvimento
pip install -e ".[dev]"

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env conforme necessário (tokens são opcionais para uso básico)
```

Após a instalação, o comando `pegada` ficará disponível no PATH do ambiente virtual.

---

## Variáveis de ambiente (`.env`)

| Variável | Obrigatória | Descrição |
|---|---|---|
| `PEGADA_DB` | Não | Caminho do banco SQLite (padrão: `data/pegada.sqlite3`) |
| `PEGADA_OUTPUT` | Não | Diretório de saídas (padrão: `output/`) |
| `GITHUB_TOKEN` | Não | Token pessoal do GitHub para maior limite de requisições |
| `NOTION_TOKEN` | Só para Notion | Token da integração no Notion |
| `NOTION_DATA_SOURCE_ID` | Só para Notion | ID da fonte de dados do Notion |
| `NOTION_DATABASE_ID` | Compatibilidade | ID do database Notion (alternativa ao item acima) |

---

## Comandos Make disponíveis

```bash
make install   # Instala o pacote em modo editável com dependências de dev
make test      # Executa a suíte completa de testes (pytest -q)
make lint      # Verifica o estilo do código (ruff check .)
make demo      # Demonstração offline: init → import-seed → export → report
make clean     # Remove todos os arquivos da pasta output/
```

---

## Comandos da CLI (`pegada`)

### `pegada init`
Inicializa o banco de dados SQLite e cria o diretório de saídas.
```bash
pegada init
```

### `pegada import-seed <path>`
Importa um conjunto inicial de evidências a partir de um arquivo JSON.
```bash
pegada import-seed data/seed/evidencias_iniciais.json
```

### `pegada import-csv <path> --kind <tipo>`
Importa evidências a partir de um arquivo CSV.
`--kind` aceita: `citation`, `book` ou qualquer categoria do modelo.
```bash
pegada import-csv data/import/google_scholar.csv --kind citation
pegada import-csv data/import/biblioteca_nacional.csv --kind book
```

### `pegada collect [--config <path>]`
Executa todos os coletores habilitados no arquivo de configuração TOML.
O padrão é `config/collector.toml`.
```bash
pegada collect --config config/collector.toml
```

### `pegada export [--all]`
Exporta evidências para `output/`.
Sem `--all`: apenas `evidencias.json`.
Com `--all`: também gera `evidencias.csv` e `mapa_pegada_digital.md`.
```bash
pegada export --all
```

### `pegada report [--format pdf]`
Gera o relatório PDF em `output/Mapa_Pegada_Digital_Aridio_Silva_Gerado.pdf`.
```bash
pegada report --format pdf
```

### `pegada notion-sync [--dry-run] [--only-reviewed]`
Sincroniza evidências com o Notion.
- `--dry-run`: exibe o que seria enviado sem gravar nada.
- `--only-reviewed`: envia apenas evidências com `identity_status = reviewed`.
```bash
# Simulação segura (recomendado antes do primeiro envio real)
pegada notion-sync --dry-run --only-reviewed

# Envio real
pegada notion-sync --only-reviewed
```

---

## Fluxo de execução completo

```bash
pegada init
pegada import-seed data/seed/evidencias_iniciais.json
pegada collect --config config/collector.toml
pegada export --all
pegada report --format pdf
```

Para demonstração offline (sem acesso à internet):
```bash
pegada init
pegada import-seed data/seed/evidencias_iniciais.json
pegada export --all
pegada report --format pdf
```

---

## Testes

A suíte usa **pytest** e cobre modelos, banco de dados, exportações e
sincronização com o Notion. Os testes usam diretórios temporários e clientes
simulados — não gravam no SQLite do projeto nem fazem chamadas externas reais.

```bash
# Executar todos os testes
pytest -q

# Executar apenas um módulo
pytest tests/test_notion_sync.py -q

# Executar com saída detalhada
pytest -v
```

### Cobertura por módulo de teste

| Arquivo | O que cobre |
|---|---|
| `tests/test_models.py` | Modelos e normalização de evidências |
| `tests/test_db.py` | Persistência SQLite e trilha de auditoria |
| `tests/test_exporters.py` | Exportações JSON, CSV e Markdown |
| `tests/test_notion_sync.py` | Idempotência, esquema e modo `--dry-run` do Notion |

> Os coletores de fontes externas (GitHub, OpenAlex, web) precisam ser
> verificados manualmente, pois dependem de disponibilidade e políticas de
> serviços externos.

---

## Lint e estilo de código

O projeto usa **ruff** com limite de 100 caracteres e target `py311`.

```bash
# Verificar
ruff check .

# Corrigir automaticamente (quando seguro)
ruff check . --fix
```

A configuração está em `pyproject.toml` na seção `[tool.ruff]`.

---

## Integração Contínua (CI)

O workflow `.github/workflows/tests.yml` é disparado em toda pull request e em
pushes à `main`. Ele executa em `ubuntu-latest` com Python 3.11 e roda:

```
pip install -e ".[dev]"
pytest
ruff check .
```

A branch `main` exige que o job `test` passe antes de qualquer merge.
Force push e deleção da branch estão bloqueados por ruleset.

---

## Dependências do projeto

### Produção (`[project.dependencies]`)

| Pacote | Versão | Uso |
|---|---|---|
| `reportlab` | `>=4.2,<5` | Geração de PDF |
| `python-dotenv` | `>=1.0,<2` | Leitura do arquivo `.env` |

### Opcionais (`[project.optional-dependencies]`)

| Extra | Pacote | Versão | Uso |
|---|---|---|---|
| `notion` | `notion-client` | `>=3.1,<4` | Sincronização com o Notion |
| `dev` | `pytest` | `>=8,<9` | Execução dos testes |
| `dev` | `ruff` | `>=0.6,<1` | Lint e formatação |

Para instalar o extra do Notion:
```bash
pip install -e ".[notion]"
```

---

## Estrutura de diretórios relevante para o build

```
Digital_Footprint_Map/
├── pyproject.toml          # Metadados, dependências e configuração do pacote
├── Makefile                # Atalhos para tarefas comuns
├── .env.example            # Modelo de variáveis de ambiente
├── config/
│   └── collector.toml      # Fontes e parâmetros dos coletores
├── src/pegada/             # Código-fonte do pacote instalável
├── tests/                  # Suíte de testes automatizados
├── data/
│   ├── import/             # CSVs para importação manual
│   └── seed/               # Evidências iniciais para demonstração
└── output/                 # Saídas geradas (não versionadas, exceto .gitkeep)
```

---

## Notas de segurança e ética

- Não inclua tokens reais no `.env` versionado; use sempre `.env.example` como modelo.
- O coletor respeita `robots.txt`, limita a taxa de requisições e não contorna autenticação.
- Resultados coletados são candidatos — revise a identidade antes de publicar.
- Consulte `docs/METODOLOGIA.md` e `docs/INTEGRACAO_NOTION.md` para diretrizes completas.
