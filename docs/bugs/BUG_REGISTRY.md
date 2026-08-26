# Bug Registry — Mapa da Pegada Digital

Índice central de todos os bugs registrados no projeto.
Atualizar sempre que um novo bug for encontrado ou um status mudar.

## Regras

- IDs são sequenciais, iniciando em `BUG-00001`, sem lacunas nem reutilização.
- Cada bug tem um arquivo dedicado em `docs/bugs/BUG-XXXXX.md`.
- Status permitidos: `Open` | `Fixed` | `Verified` | `Wontfix`.
- Severidade: `Critical` | `High` | `Medium` | `Low`.

---

## Índice

| ID | Título | Componente | Severidade | Status | Corrigido em |
|---|---|---|---|---|---|
| [BUG-00001](./BUG-00001.md) | Whitespace em `confidence` CSV causa ValueError | `src/pegada/importers.py` (F-0004) | Medium | Verified | PR #7 |
