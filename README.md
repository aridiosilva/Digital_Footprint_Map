# Gerador do Mapa da Pegada Digital

Projeto reproduzível para coletar, registrar, revisar e publicar evidências públicas sobre a pegada digital de Aridio Silva. O pacote separa a **coleta de dados** da **geração do relatório**.

## O que está incluído

- coletores para páginas web, GitHub e OpenAlex;
- importação manual de resultados do Google Acadêmico e da Biblioteca Nacional;
- banco SQLite com trilha de auditoria e hashes;
- normalização, deduplicação e revisão de identidade;
- exportação JSON, CSV e Markdown;
- geração de PDF;
- relatórios anteriores em `docs/relatorios/`;
- dados bibliográficos iniciais e referências conhecidas;
- conector opcional do Notion, desativado por padrão;
- testes automatizados e exemplo de execução.

O software coleta apenas conteúdo publicamente acessível e não tenta contornar login, CAPTCHA, robots.txt ou bloqueios. Resultados devem ser revisados por uma pessoa antes da publicação, sobretudo para evitar homônimos.

## Instalação

Requer Python 3.11 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
cp .env.example .env
```

## Uso rápido

```bash
pegada init
pegada import-seed data/seed/evidencias_iniciais.json
pegada collect --config config/collector.toml
pegada export --all
pegada report --format pdf
```

Saídas são gravadas em `output/`. Para uma demonstração offline:

```bash
pegada init && pegada import-seed data/seed/evidencias_iniciais.json
pegada export --all && pegada report --format pdf
```

## Google Acadêmico e Biblioteca Nacional

O projeto não raspa automaticamente o Google Acadêmico. Exporte/registre os resultados confirmados em `data/import/google_scholar.csv`. Registros da Biblioteca Nacional podem ser inseridos em `data/import/biblioteca_nacional.csv`. Depois execute:

```bash
pegada import-csv data/import/google_scholar.csv --kind citation
pegada import-csv data/import/biblioteca_nacional.csv --kind book
```

## Notion (posteriormente)

Quando desejar, defina `NOTION_TOKEN` e `NOTION_DATABASE_ID` no `.env`, instale o extra `notion` e execute `pegada notion-sync`. Nada é enviado ao Notion sem esse comando explícito.

## Estrutura do Projeto

```text
Digital_Footprint_Map/
├── .env.example                         # Modelo de variáveis de ambiente e credenciais opcionais.
├── .gitignore                           # Arquivos locais e dados gerados que não devem ser versionados.
├── LICENSE                              # Licença de uso do projeto.
├── Makefile                             # Atalhos para instalação, testes e execução das tarefas comuns.
├── pyproject.toml                       # Metadados, dependências e configuração do pacote Python.
├── README.md                            # Visão geral, instalação, uso e orientações do projeto.
│
├── config/
│   └── collector.toml                   # Fontes públicas e parâmetros configuráveis dos coletores.
│
├── data/
│   ├── import/
│   │   ├── biblioteca_nacional.csv      # Registros bibliográficos importados manualmente.
│   │   └── google_scholar.csv           # Citações e obras confirmadas para importação manual.
│   ├── seed/
│   │   └── evidencias_iniciais.json     # Conjunto inicial de evidências para demonstração offline.
│   └── pegada.sqlite3                   # Banco SQLite local com evidências e trilha de auditoria.
│
├── docs/
│   ├── ARQUITETURA.md                   # Arquitetura e componentes do sistema.
│   ├── DICIONARIO_DE_DADOS.md           # Campos, entidades e significado dos dados coletados.
│   ├── MAPA_DO_COLETOR.md               # Fluxo e escopo dos coletores de evidências.
│   ├── METODOLOGIA.md                   # Critérios de coleta, revisão e validação das evidências.
│   └── relatorios/
│       ├── Mapa_Pegada_Digital_Aridio_Silva.pdf
│       │                                # Relatório PDF de referência do mapa digital.
│       └── Mapa_Pegada_Digital_Aridio_Silva_Atualizado_Bibliografia.pdf
│                                        # Relatório PDF com bibliografia e citações atualizadas.
│
├── output/
│   ├── .gitkeep                         # Mantém o diretório de saídas no repositório.
│   ├── evidencias.csv                   # Exportação tabular de evidências gerada pela CLI.
│   ├── evidencias.json                  # Exportação JSON de evidências gerada pela CLI.
│   ├── mapa_pegada_digital.md           # Relatório Markdown gerado.
│   └── Mapa_Pegada_Digital_Aridio_Silva_Gerado.pdf
│                                        # Relatório PDF gerado a partir das evidências.
│
├── src/
│   └── pegada/
│       ├── __init__.py                  # Identifica o pacote Python.
│       ├── cli.py                       # Comandos da interface de linha de comando `pegada`.
│       ├── collectors.py                # Coleta conteúdo de fontes públicas autorizadas.
│       ├── config.py                    # Leitura e validação das configurações.
│       ├── db.py                        # Persistência SQLite e trilha de auditoria.
│       ├── exporters.py                 # Exportação de evidências em JSON, CSV e Markdown.
│       ├── importers.py                 # Importação de dados CSV e conjuntos iniciais.
│       ├── models.py                    # Modelos e normalização das entidades de evidência.
│       ├── notion_sync.py               # Integração opcional e explícita com o Notion.
│       └── report.py                    # Geração dos relatórios do mapa da pegada digital.
│
└── tests/
    ├── test_db.py                       # Testes da persistência e auditoria no SQLite.
    ├── test_exporters.py                # Testes das exportações de dados e relatórios.
    └── test_models.py                   # Testes dos modelos e da normalização de evidências.
```

Consulte também `docs/ARQUITETURA.md`, `docs/MAPA_DO_COLETOR.md`,
`docs/METODOLOGIA.md` e `docs/DICIONARIO_DE_DADOS.md` para detalhes.

## Aviso

Ferramenta de OSINT defensiva e autoconsulta. Respeite LGPD, direitos autorais, termos dos sites e pedidos de remoção. URLs e trechos são evidências; não representam confirmação automática de identidade.
