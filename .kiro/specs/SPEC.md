# SPEC.md — Mapa da Pegada Digital

> Documento raiz da especificação do projeto. Gerado por engenharia reversa a
> partir da versão 1.1.0 do código-fonte para alinhar o repositório ao padrão
> Spec-Driven Development. A partir desta versão, toda nova feature ou bugfix
> deve seguir o fluxo: Requirements → Design → Tasks antes da implementação.

---

## Visão do Produto

Ferramenta auditável de OSINT defensiva e autoconsulta que coleta, registra,
revisa e publica evidências **públicas** sobre a pegada digital de uma pessoa
física (uso inicial: Aridio Silva). O sistema separa coleta de dados da
geração de relatórios e mantém trilha de auditoria completa.

## Objetivos

1. Coletar automaticamente evidências públicas de múltiplas fontes (GitHub,
   OpenAlex, páginas web).
2. Importar manualmente fontes que não permitem coleta automática (Google
   Acadêmico, Biblioteca Nacional).
3. Persistir evidências num banco SQLite auditável com deduplicação por SHA-256.
4. Exportar evidências em JSON, CSV e Markdown.
5. Gerar relatório PDF formatado.
6. Sincronizar evidências revisadas com uma fonte de dados do Notion de forma
   idempotente e explícita.
7. Expor todas as operações via CLI unificada (`pegada`).

## Princípios

- **Auditabilidade**: toda evidência tem fingerprint, data de coleta e status.
- **Isolamento de falhas**: um coletor falho não interrompe os demais.
- **Idempotência**: re-execuções não duplicam dados (banco e Notion).
- **Revisão humana obrigatória**: resultados automáticos são candidatos.
- **Ética e LGPD**: apenas dados públicos, respeito a robots.txt e remoções.

## Versão atual

`1.1.0` — todas as features listadas abaixo estão implementadas.

---

## Features implementadas (índice de specs)

| ID | Feature | Status | Spec |
|---|---|---|---|
| F-01 | Evidence Model & Fingerprint | ✅ Implementado | [evidence-model](./evidence-model/requirements.md) |
| F-02 | Auditable SQLite Database | ✅ Implementado | [auditable-database](./auditable-database/requirements.md) |
| F-03 | Evidence Collectors | ✅ Implementado | [evidence-collectors](./evidence-collectors/requirements.md) |
| F-04 | Evidence Importers (CSV/JSON) | ✅ Implementado | [evidence-importers](./evidence-importers/requirements.md) |
| F-05 | Evidence Exporters (JSON/CSV/MD) | ✅ Implementado | [evidence-exporters](./evidence-exporters/requirements.md) |
| F-06 | PDF Report Generator | ✅ Implementado | [pdf-report](./pdf-report/requirements.md) |
| F-07 | Notion Sync | ✅ Implementado | [notion-sync](./notion-sync/requirements.md) |
| F-08 | CLI Interface | ✅ Implementado | [cli-interface](./cli-interface/requirements.md) |
| BUG-REGISTRY | Bug Documentation Standard | ✅ Implementado | [bug-registry](./bug-registry/requirements.md) |

---

## Fluxo de desenvolvimento (a partir desta versão)

```
Nova feature / bugfix
        │
        ▼
requirements.md  ──▶  design.md  ──▶  tasks.md  ──▶  Implementação  ──▶  Testes
        │
   (revisão humana a cada etapa)
```

Todos os arquivos de spec ficam em `.kiro/specs/{feature-name}/`.

---

## Estrutura de diretórios da especificação

```
.kiro/
├── specs/
│   ├── SPEC.md                        ← este arquivo
│   ├── evidence-model/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── auditable-database/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── evidence-collectors/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── evidence-importers/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── evidence-exporters/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── pdf-report/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   ├── notion-sync/
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   └── cli-interface/
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
└── steering/
    └── project-conventions.md         ← padrões e convenções do projeto
```

---

## Bug Registry

Todos os bugs encontrados são documentados em `docs/bugs/`.

- Índice central: [docs/bugs/BUG_REGISTRY.md](../../docs/bugs/BUG_REGISTRY.md)
- Formato de ID: `BUG-XXXXX` (cinco dígitos, sequencial a partir de BUG-00001)

| ID | Título | Status |
|---|---|---|
| [BUG-00001](../../docs/bugs/BUG-00001.md) | Whitespace em confidence CSV causa ValueError | Verified |

