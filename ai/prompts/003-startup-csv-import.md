# 003 - Importação automática e idempotente do CSV na subida da aplicação

## Objetivo

Fechar o requisito não-funcional do SPECS.md que pedia carregamento do
CSV na subida da aplicação, sem passos manuais: usar o `lifespan` do
FastAPI para criar as tabelas e importar `data/Movielist.csv`
automaticamente, de forma idempotente (não reimportar/duplicar se o
banco já tiver filmes), e adaptar os testes para cobrir esse
comportamento sem tocar o `movies.db` real.

## Prompt utilizado

Obrigado por ter identificado e lembrado do requisito funcional descrito no `SPECS.md` sobre importar o CSV ao iniciar a aplicação.

Faça as seguintes alterações:

1. **Inicialização da aplicação**

   * Adaptar o projeto para que, ao iniciar o FastAPI, o banco seja criado caso necessário e o `data/Movielist.csv` seja importado automaticamente.
   * Usar o mecanismo `lifespan` do FastAPI.
   * A importação deve ser idempotente: se o banco já possuir filmes, não importar novamente nem duplicar registros.
   * Manter o `scripts/import_csv.py` reutilizável.

2. **Testes**

   * Reescrever/adaptar os testes existentes para contemplar essa nova inicialização.
   * Garantir que os testes utilizem banco isolado e nunca alterem o `movies.db` real.
   * Testar também o comportamento de inicialização:

     * banco vazio → CSV é importado;
     * banco já populado → CSV não é importado novamente;
     * os registros não são duplicados.
   * Manter os testes unitários da regra de intervalos e os testes de integração da API.

3. **Documentação de IA**

   * Registrar a alteração e a decisão tomada dentro de `ai/`.
   * Antes de documentar, leia e siga a skill:
     `.claude/skills/document-ai/SKILL.md`.

4. **README**

   * Atualizar o `README.md` para refletir o comportamento atual da aplicação, incluindo a importação automática do CSV durante a inicialização e a proteção contra duplicação.
   * Atualizar também a seção de testes/status do projeto para não deixar informações desatualizadas.

Antes de alterar qualquer arquivo, analise `SPECS.md`, `CLAUDE.md`, `README.md`, `ai/` e a estrutura atual do projeto.

Mantenha a arquitetura simples e consistente com o projeto atual. Não introduza repositories, interfaces ou outras abstrações desnecessárias.

Ao finalizar, execute a suíte completa de testes e informe o resultado.

## Resultado produzido pela IA

- `app/main.py`: adicionado `lifespan` (via `@asynccontextmanager`) que
  chama `create_tables_and_import_movies()` — cria as tabelas
  (`Base.metadata.create_all`) e importa o CSV
  (`scripts.import_csv.import_movies`) — antes de a API começar a
  responder.
- `scripts/import_csv.py`: `import_movies()` agora verifica se já existe
  algum filme no banco antes de importar (`db.query(Movie).first()`);
  se sim, ignora a importação e retorna. Também passou a acessar
  `database.SessionLocal` via `from app import database` (em vez de
  `from app.database import SessionLocal`), para poder ser
  redirecionado a um banco isolado em testes.
- `tests/conftest.py`: fixture `client` deixou de usar
  `with TestClient(app)`, evitando disparar o `lifespan` (que tentaria
  importar o CSV no `movies.db` real, já que essa fixture só sobrescreve
  `get_db`, não `app.database.engine`).
- `tests/test_startup.py` (novo): testa o `lifespan` de fato, com um
  banco isolado obtido substituindo `app.database.engine`/`SessionLocal`
  via `monkeypatch` antes de entrar no `TestClient` como context
  manager. Cobre: banco vazio → CSV importado (206 filmes, intervalos
  corretos); banco já populado → importação ignorada, sem duplicar;
  `import_movies()` chamado duas vezes não duplica registros.
- `README.md` e `SPECS.md`: atualizados para refletir a importação
  automática/idempotente, os scripts manuais como opcionais, e os
  quatro níveis de teste (incluindo o de inicialização).

## Revisão e decisões técnicas

- Em vez de introduzir uma abstração de repositório/factory para
  injetar o banco no `lifespan`, optei por fazer `create_tables_and_import_movies()`
  e `import_movies()` lerem `app.database.engine`/`SessionLocal` por
  atributo do módulo (não por `from ... import` no topo do arquivo).
  Isso permite que os testes troquem esses atributos com `monkeypatch`
  antes de disparar o `lifespan`, sem precisar de nenhuma camada nova —
  mantém a arquitetura simples pedida no CLAUDE.md.
- Confirmei experimentalmente que o `TestClient` da Starlette só dispara
  `lifespan` quando usado como context manager (`with TestClient(app)`);
  usá-lo diretamente (`TestClient(app)`) não dispara startup/shutdown.
  Por isso a fixture `client` (usada pelos testes de CRUD e do dataset)
  passou a evitar o `with`, preservando o comportamento anterior desses
  testes sem qualquer risco de tocar o `movies.db` real; só
  `tests/test_startup.py` usa `with TestClient(app)` deliberadamente,
  sobre um banco já isolado.
- `scripts/create_database.py` não foi alterado nem passou a ser
  chamado pelo `lifespan` (que cria as tabelas inline com
  `Base.metadata.create_all`), para evitar reexecutar um script com
  efeito colateral de import a cada subida — ele continua disponível
  como utilitário manual opcional.

## Problemas encontrados e correções

- Validação manual (fora do pytest) foi necessária para confirmar dois
  comportamentos que os testes não cobrem sozinhos com a mesma força de
  evidência: subir a API de verdade (`uvicorn`) contra um banco novo
  populou 206 filmes e calculou os intervalos corretamente; subindo de
  novo sobre o mesmo banco, o log mostrou
  "Banco já possui filmes importados; importação ignorada." e a
  contagem de filmes permaneceu 206 (sem duplicar). Isso foi feito numa
  cópia do projeto em `/tmp`, sem tocar o repositório.

## Validação

- `uv run pytest -v`: 26 testes, todos passando (23 anteriores + 3 novos
  em `tests/test_startup.py`).
- `stat` no `movies.db` de desenvolvimento antes/depois da suíte
  confirmou que ele não foi modificado pelos testes.
- Smoke test manual com `uvicorn` (fora do repositório, em `/tmp`):
  banco novo → `GET /movies/` retorna 206 filmes e
  `GET /movies/producers/awards` retorna o resultado esperado
  (Joel Silver, 1990→1991 / Matthew Vaughn, 2002→2015); reiniciar o
  servidor sobre o mesmo banco manteve 206 filmes, sem duplicar.
