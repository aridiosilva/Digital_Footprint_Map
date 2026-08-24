# Arquitetura

```mermaid
flowchart TD
    A[Configuração e sementes] --> B[Coletores]
    B --> C[Normalização e Evidence]
    C --> D[(SQLite)]
    D --> E[Revisão de identidade]
    E --> F[JSON / CSV / Markdown]
    E --> G[PDF]
    E -. comando opcional .-> H[Notion]
```

O `fingerprint` SHA-256 impede duplicação exata por URL, título e categoria. O status de identidade começa como `pending`; apenas evidências revisadas devem receber `reviewed`. Coletores falham isoladamente para que uma origem indisponível não interrompa as demais.
