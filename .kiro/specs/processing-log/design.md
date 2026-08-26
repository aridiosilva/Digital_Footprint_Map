# Design — PROC-LOG: Processing Log Standard

## Directory Structure

```
docs/
└── logs/
    └── LOG_PROCESSAMENTO_26082026.md    ← initial log (today)
```

---

## Log File Template

```markdown
# LOG DE PROCESSAMENTO — DD/MM/AAAA

## Resumo da sessão

| Campo | Valor |
|---|---|
| Data | DD/MM/AAAA |
| Operador | Kiro (IA) / [nome humano] |
| Sessão | N |
| Início | HH:MM UTC |
| Duração estimada | Xmin |

---

## Sessão N — [breve título]

### Contexto
[Por que esta sessão foi iniciada]

### Tarefas executadas

| # | Tarefa | Status | Artefatos |
|---|---|---|---|
| 1 | ... | ✅ | ... |

### Bugs encontrados
- BUG-XXXXX: [título]

### PRs
- PR #N — [título] — merged/open

### Decisões tomadas
- ...

### Notas
- ...
```

---

## Naming Helper

Given today = 26 August 2026:
- DD = 26, MM = 08, AAAA = 2026
- Filename = `LOG_PROCESSAMENTO_26082026.md`

---

## Integration with Bug Registry and Feature IDs

Log entries MUST reference:
- Feature IDs as `F-XXXX` (four-digit format)
- Bug IDs as `BUG-XXXXX` (five-digit format)
- PRs as `PR #N`

This makes logs machine-searchable for cross-referencing.
