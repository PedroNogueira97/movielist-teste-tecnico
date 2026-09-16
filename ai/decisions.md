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

## Banco de teste SQLite em memória, isolado do movies.db

Testes de integração (`tests/conftest.py`) usam um banco SQLite em
memória (`sqlite://` + `StaticPool`), criado e descartado a cada teste,
em vez de reutilizar `movies.db` ou criar um arquivo `.db` de teste em
disco. Motivo: evita qualquer risco de os testes alterarem dados de
desenvolvimento e não deixa arquivos residuais; `StaticPool` garante que
todas as conexões da mesma sessão de teste enxerguem o mesmo banco em
memória.

Referência: [001 - Estrutura inicial do projeto](prompts/001-project-structure.md),
[002 - Suíte de testes](prompts/002-test-suite.md)
