# SPECS.md

Requisitos conhecidos do teste técnico. Este documento é a fonte de
verdade de escopo — ver regra correspondente em [CLAUDE.md](CLAUDE.md).

## Objetivo

Disponibilizar, via API REST, os dados de indicados e vencedores da
categoria **Pior Filme** do Golden Raspberry Awards, permitindo identificar
o(s) produtor(es) com o **maior** e o **menor** intervalo entre dois
prêmios consecutivos.

## Dados de entrada

- Arquivo `data/Movielist.csv` (confirmado — 206 filmes, 1980 a 2019),
  importado para o banco (SQLite) automaticamente na subida da aplicação
  (`lifespan` do FastAPI em `app/main.py`, que cria as tabelas e chama
  `scripts/import_csv.py:import_movies`) — não depende mais de rodar
  scripts manualmente. Ver [README.md](README.md).
- Separador `;` e encoding `utf-8-sig` (confirmado).
- Colunas do CSV (confirmado, cabeçalho real):
  `year;title;studios;producers;winner`.
  - `year`: inteiro, ano da cerimônia.
  - `title`: string, título do filme.
  - `studios`: string com um ou mais estúdios separados por vírgula —
    normalizado para lista de strings na importação
    (`normalize_studios` em `scripts/import_csv.py`).
  - `producers`: string com um ou mais produtores separados por vírgula
    e/ou " and " — normalizado para lista de strings na importação
    (`normalize_producers` em `scripts/import_csv.py`).
  - `winner`: `"yes"` para filme vencedor da categoria naquele ano, ou
    vazio caso contrário — normalizado para booleano na importação
    (`normalize_winner` em `scripts/import_csv.py`).
- Apenas filmes com `winner = true` entram no cálculo de intervalo entre
  prêmios.

## Endpoint principal (formato conhecido do teste)

`GET /movies/producers/awards` (nome de rota confirmado/implementado em
`app/api/routes/movies.py`).

Resposta esperada (confirmada, ver `app/schemas/movie.py` e
`app/services/producer_awards.py`):

```json
{
  "min": [
    {
      "producer": "string",
      "interval": 0,
      "previousWin": 0,
      "followingWin": 0
    }
  ],
  "max": [
    {
      "producer": "string",
      "interval": 0,
      "previousWin": 0,
      "followingWin": 0
    }
  ]
}
```

- `min`: produtor(es) com o menor intervalo entre duas vitórias
  consecutivas.
- `max`: produtor(es) com o maior intervalo entre duas vitórias
  consecutivas.
- Pode haver mais de um produtor empatado em `min` e/ou `max` — a lista
  deve conter todos os empates.

## Requisitos não-funcionais conhecidos

- Banco de dados deve ser carregado em memória/arquivo a partir do CSV na
  subida da aplicação (sem depender de migrações manuais para rodar o
  teste) — **atendido**: `app/main.py` registra um `lifespan` que cria as
  tabelas (`Base.metadata.create_all`) e importa `data/Movielist.csv`
  automaticamente ao subir a API, de forma idempotente (banco já populado
  não é reimportado, sem duplicar registros). Ver
  `tests/test_startup.py`.
- Aplicação deve subir e responder sem passos manuais além de instalar
  dependências e rodar o servidor — **atendido**, mesma implementação
  acima (`uv sync` + `uv run uvicorn app.main:app --reload`).
- Testes automatizados (pytest) devem validar o resultado do endpoint
  principal contra o dataset fornecido — **atendido**
  (`tests/test_producer_awards_dataset.py`, carrega
  `data/Movielist.csv` inteiro em banco de teste isolado e valida a
  resposta completa do endpoint; `tests/test_startup.py` valida o mesmo
  resultado passando pelo `lifespan` real da aplicação).

## Em aberto / a confirmar

- Rotas adicionais além do CRUD de filmes e do endpoint de intervalos
  (filtros, paginação etc.) — só serão adicionadas se especificadas.

## Confirmado

- Dataset real: `data/Movielist.csv`, separador `;`, encoding
  `utf-8-sig`, colunas `year;title;studios;producers;winner`.
- Nome da rota principal: `GET /movies/producers/awards`.
- Nenhum empate real existe no dataset fornecido: o menor intervalo é de
  Joel Silver (1 ano, 1990→1991) e o maior é de Matthew Vaughn (13 anos,
  2002→2015) — mas a lógica de empate está implementada e coberta por
  teste (`tests/test_producer_awards.py`) para o caso de outros datasets.

## O que já foi implementado

- [x] Modelo SQLAlchemy de filme (`app/models/movie.py`)
- [x] Configuração de engine/sessão (`app/database.py`)
- [x] Script de criação do banco (`scripts/create_database.py`)
- [x] Script de importação do CSV (`scripts/import_csv.py`)
- [x] Schemas Pydantic de entrada/saída (`app/schemas/movie.py`)
- [x] Serviço de cálculo de intervalos por produtor
      (`app/services/producer_awards.py`)
- [x] Rotas da API (`app/api/routes/movies.py`), incluindo CRUD de
      filmes e `GET /movies/producers/awards`, registradas em
      `app/main.py`
- [x] Testes unitários da lógica de negócio
      (`tests/test_producer_awards.py`): maior/menor intervalo, empate,
      múltiplos produtores, produtor com um único prêmio, filmes não
      vencedores
- [x] Testes de integração da API (`tests/test_movies.py`): fluxos CRUD
      e códigos HTTP `200`/`201`/`204`/`404`/`422`, com banco de teste
      isolado (`tests/conftest.py`)
- [x] Teste de integração final com o dataset real
      (`tests/test_producer_awards_dataset.py`)
- [x] Carregamento automático e idempotente do CSV na subida da
      aplicação via `lifespan` do FastAPI (`app/main.py`)
- [x] Testes da inicialização da aplicação (`tests/test_startup.py`):
      banco vazio importa o CSV, banco já populado não reimporta,
      `import_movies()` chamado duas vezes não duplica registros

## O que ainda falta

Nenhum item pendente no momento. Novas funcionalidades só serão
adicionadas se especificadas neste documento.
