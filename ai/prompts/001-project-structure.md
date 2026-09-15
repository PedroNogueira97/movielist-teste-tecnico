# 001 - Estrutura inicial do projeto

## Objetivo

Criar a estrutura inicial do projeto (API REST FastAPI para o Golden
Raspberry Awards) e a documentação de contexto/especificação, sem
implementar nenhuma lógica de negócio.

## Prompt utilizado

Quero estruturar este projeto como um teste técnico de uma API REST com FastAPI para o Golden Raspberry Awards.

Antes de implementar qualquer lógica de negócio, quero criar a estrutura inicial do projeto e a documentação.

Stack:

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* pytest
* uv

Quero uma estrutura simples, sem DDD ou Clean Architecture exagerada:

```text
app/
├── main.py
├── database.py
├── models/
│   └── movie.py
├── schemas/
│   └── movie.py
├── services/
│   └── producer_awards.py
└── api/
    └── routes/
        └── movies.py

tests/
├── test_movies.py
└── test_producer_awards.py

scripts/
└── import_csv.py

data/
└── movies.csv

ai/
├── README.md
├── decisions.md
└── prompts/
```

Crie também:

* `CLAUDE.md`
* `SPECS.md`
* `ai/README.md`
* `ai/decisions.md`

No `CLAUDE.md`, documente o contexto do projeto e regras simples de desenvolvimento:

* manter a arquitetura simples;
* não adicionar abstrações sem necessidade;
* lógica de negócio em `services`;
* acesso ao banco separado das rotas;
* usar type hints;
* escrever testes para a lógica de negócio;
* não adicionar dependências sem necessidade;
* seguir PEP 8;
* não implementar funcionalidades que não estejam especificadas.

Também quero criar uma skill para documentar o uso de IA neste projeto.

Crie uma skill em:

```text
.claude/skills/document-ai/
└── SKILL.md
```

Essa skill deve ser usada sempre que uma tarefa relevante for concluída com auxílio da IA.

Ela deve orientar o agente a registrar a interação na pasta:

```text
ai/
├── README.md
├── decisions.md
└── prompts/
    ├── 001-project-structure.md
    ├── 002-csv-import.md
    ├── 003-producer-intervals.md
    └── 004-tests.md
```

Os arquivos dentro de `prompts/` devem ser numerados sequencialmente conforme novas tarefas forem documentadas.

Cada registro deve conter, de forma objetiva:

* objetivo da tarefa;
* prompt utilizado;
* resultado produzido pela IA;
* minha revisão/decisões técnicas, quando relevante;
* problemas encontrados e correções solicitadas;
* validação realizada, como testes ou comandos executados.

Não quero salvar dumps gigantes de conversas. A documentação deve ser um registro resumido e legível do processo de desenvolvimento com IA.

A skill também deve orientar o agente a atualizar `ai/README.md` quando necessário, mantendo uma lista dos registros existentes e das ferramentas/skills de IA utilizadas no projeto.

O `ai/README.md` deve explicar brevemente por que essa pasta existe, quais ferramentas de IA foram utilizadas e como os registros estão organizados.

No `SPECS.md`, documente de forma objetiva os requisitos conhecidos do teste e deixe claro o que ainda precisa ser implementado.

Crie apenas o esqueleto inicial e a documentação. Não implemente nenhuma lógica de negócio ainda.

Também não crie endpoints completos, queries, importação real do CSV ou cálculo dos intervalos neste momento.

## Resultado produzido pela IA

- Estrutura de pastas: `app/{main.py,database.py,models/,schemas/,
  services/,api/routes/}`, `tests/`, `scripts/import_csv.py`,
  `data/movies.csv` (vazio) — todos os módulos como esqueleto (docstring
  "Not implemented yet", sem lógica).
- `CLAUDE.md`: contexto do projeto e regras de desenvolvimento.
- `SPECS.md`: requisitos conhecidos do teste (endpoint, formato de
  resposta, dados de entrada) e checklist do que falta implementar.
- `.gitignore` (não existia).
- `.claude/skills/document-ai/SKILL.md`: skill para registrar tarefas
  feitas com IA em `ai/`.
- `ai/README.md` e `ai/decisions.md`.
- `pyproject.toml` ajustado: dependências do stack
  (fastapi, uvicorn, sqlalchemy, pydantic) e grupo `dev`
  (pytest, httpx); projeto marcado como `package = false`.

## Revisão e decisões técnicas

- Removidos `src/movie_list_teste_tecnico/` (scaffold default do
  `uv init`, não usado) e a pasta `ia/` (nome em português, criada vazia
  em tentativa anterior) — nenhum dos dois estava versionado nem continha
  conteúdo.
- `app/main.py` original (stub "Hello, world!") substituído por app
  FastAPI mínima com apenas `/health`, sem rotas de negócio.
- Ver decisões detalhadas em [decisions.md](../decisions.md).

## Problemas encontrados e correções

- Primeira tentativa de `uv sync` foi bloqueada pelo classificador de
  permissões do ambiente; na segunda tentativa (com aprovação do
  usuário) rodou normalmente e atualizou `uv.lock`.

## Validação

- `uv sync` — instalou sqlalchemy, pydantic (via fastapi), pytest e
  httpx sem erros.
- `uv run pytest -q` — coleta sem erros (0 testes, esperado: arquivos de
  teste ainda são só esqueleto).
- `uv run python -c "from app.main import app; print(app.title)"` —
  aplicação FastAPI importa e instancia corretamente.
- Validação manual: inspeção da árvore de diretórios criada
  (`find . -not -path '*/.git*' -not -path '*/.venv*'`) conferindo
  contra a estrutura pedida.
