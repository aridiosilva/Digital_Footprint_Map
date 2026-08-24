# Integração com o Notion

## Objetivo

Publicar as evidências armazenadas no SQLite em uma fonte de dados do Notion.
A integração cria registros novos e atualiza os existentes usando o
`Fingerprint` SHA-256, evitando duplicações entre execuções.

## Preparação no Notion

Crie uma integração interna, mantenha o token em segredo e conecte a integração
à página que contém a fonte de dados. Crie as colunas exatamente assim:

| Coluna | Tipo no Notion |
| --- | --- |
| Nome | Title |
| URL | Text |
| Categoria | Select |
| Fonte | Text |
| Confiança | Number |
| Status | Select |
| Fingerprint | Text |
| Trecho | Text |
| Autores | Multi-select |
| Coletado em | Date |
| Notas | Text |

`URL` é texto porque o projeto também armazena identificadores `urn:`, além de
endereços HTTP. O sincronizador valida todo o esquema antes de alterar dados.

## Configuração

Copie `.env.example` para `.env`:

```dotenv
NOTION_TOKEN=secret_...
NOTION_DATA_SOURCE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

O `NOTION_DATA_SOURCE_ID` pode ser copiado em **Manage data sources > Copy data
source ID**. Como compatibilidade, `NOTION_DATABASE_ID` também é aceito quando o
database contém exatamente uma fonte de dados.

## Execução segura

```bash
pip install -e '.[notion]'
pegada notion-sync --dry-run --only-reviewed
pegada notion-sync --only-reviewed
```

- `--dry-run`: lê e valida o destino, mas não cria nem altera páginas.
- `--only-reviewed`: publica somente evidências cujo status é `reviewed`.
- sem opções: sincroniza todas as evidências, inclusive as pendentes.

O arquivo `.env` é ignorado pelo Git. Nunca inclua o token no ZIP, em commits,
capturas de tela ou relatórios.
