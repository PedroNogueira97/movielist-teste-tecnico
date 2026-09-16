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

## Importação do CSV via lifespan, com acesso ao banco por atributo de módulo

A importação automática do CSV na subida da aplicação usa o `lifespan`
do FastAPI (`app/main.py`), e tanto `create_tables_and_import_movies()`
quanto `import_movies()` (`scripts/import_csv.py`) acessam
`app.database.engine`/`SessionLocal` por atributo de módulo
(`database.engine`, `database.SessionLocal`) em vez de importar esses
nomes diretamente no topo do arquivo. Motivo: isso permite que os testes
apontem o `lifespan` para um banco SQLite isolado usando `monkeypatch`
(`tests/test_startup.py`), sem precisar de uma camada de injeção de
dependência dedicada — mantém a arquitetura simples do projeto. Testes
que não exercitam o `lifespan` (CRUD, dataset real) evitam usar
`TestClient` como context manager, já que isso é o que dispara o
`lifespan` na Starlette; confirmado experimentalmente que instanciar
`TestClient(app)` sem `with` não dispara startup/shutdown.

A importação em si (`import_movies()`) é idempotente: verifica se já
existe algum filme no banco antes de ler o CSV, e se sim, ignora a
importação. Isso resolve tanto o caso "app reiniciada sobre banco já
populado" quanto rodar `scripts/import_csv.py` manualmente mais de uma
vez.

Referência: [003 - Importação automática e idempotente do CSV](prompts/003-startup-csv-import.md)
