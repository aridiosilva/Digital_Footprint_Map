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

## Estrutura

Consulte `docs/ARQUITETURA.md`, `docs/MAPA_DO_COLETOR.md`, `docs/METODOLOGIA.md` e `docs/DICIONARIO_DE_DADOS.md`.

## Aviso

Ferramenta de OSINT defensiva e autoconsulta. Respeite LGPD, direitos autorais, termos dos sites e pedidos de remoção. URLs e trechos são evidências; não representam confirmação automática de identidade.
