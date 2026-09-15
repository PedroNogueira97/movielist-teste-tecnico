# Decisões técnicas

Registro curto de decisões técnicas relevantes tomadas com apoio de IA.
Formato: decisão + motivo. Detalhes completos da tarefa que originou a
decisão ficam em `prompts/`.

## Estrutura de pastas simples, sem DDD/Clean Architecture

Optado por uma estrutura em camadas simples (`models`, `schemas`,
`services`, `api/routes`) em vez de Clean Architecture/DDD. Motivo:
escopo do teste técnico é pequeno e bem definido; camadas extras
adicionariam complexidade sem benefício. Ver [SPECS.md](../SPECS.md) e
[CLAUDE.md](../CLAUDE.md).

## Projeto tratado como aplicação, não como pacote distribuível

`pyproject.toml` configurado com `[tool.uv] package = false` e sem
`src/` layout. Motivo: é uma API a ser executada com `uvicorn`, não uma
biblioteca a ser instalada/publicada — o layout `src/movie_list_teste_tecnico/`
gerado pelo `uv init` foi removido por não ser usado.

## httpx como dependência de desenvolvimento

Adicionado `httpx` ao grupo `dev` do `uv`. Motivo: é dependência exigida
pelo `TestClient` do FastAPI/Starlette para os testes de API
(`tests/test_movies.py`), não uma dependência de negócio adicional.

Referência: [001 - Estrutura inicial do projeto](prompts/001-project-structure.md)
