# Mapa completo do coletor

| Etapa | Entrada | Componente | Saída |
|---|---|---|---|
| Configuração | TOML e variáveis de ambiente | `config.py` | fontes e limites |
| Coleta web | URL pública | `WebCollector` | título, resumo, URL final |
| GitHub | usuário público | `GitHubCollector` | perfil e repositórios |
| Acadêmico | consulta nominal | `OpenAlexCollector` | trabalhos candidatos |
| Importação | CSV/JSON revisado | `importers.py` | evidências estruturadas |
| Normalização | dados heterogêneos | `Evidence` | esquema único e hash |
| Persistência | evidências | `Repository` | SQLite auditável |
| Publicação | banco revisado | `exporters.py`, `report.py` | JSON, CSV, MD e PDF |
| Integração futura | banco revisado | `notion_sync.py` | páginas no banco Notion |

## Regras operacionais

1. Não contornar autenticação, CAPTCHA ou bloqueios.
2. Respeitar `robots.txt`, intervalo de requisições e termos de uso.
3. Tratar resultados nominais como candidatos até revisão de identidade.
4. Registrar URL, fonte, data, confiança e observações.
5. Não afirmar contagem do Google Acadêmico sem verificação atual.
6. Separar fato observado, inferência e declaração do titular.
