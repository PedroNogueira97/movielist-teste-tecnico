# Golden Raspberry Awards API

Teste técnico: API REST em FastAPI para consultar a lista de indicados e vencedores da categoria **Pior Filme** do Golden Raspberry Awards e identificar o(s) produtor(es) com o **maior** e o **menor** intervalo entre dois prêmios consecutivos.

> Escopo do teste técnico concluído: estrutura da aplicação, persistência dos dados, importação do dataset, operações CRUD da API e o endpoint de cálculo dos intervalos entre prêmios, com testes unitários e de integração (banco isolado e dataset real) cobrindo esses fluxos. Detalhes de escopo em [SPECS.md](SPECS.md).

## Stack

* Python 3.12
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* pytest
* [uv](https://docs.astral.sh/uv/) (dependências e ambiente)

## Estrutura

```text
app/
├── main.py                  # instancia o FastAPI e registra routers
├── database.py              # engine/session do SQLAlchemy
├── models/                  # modelos SQLAlchemy (tabelas)
├── schemas/                 # schemas Pydantic (entrada/saída da API)
├── services/                # lógica de negócio
└── api/routes/              # rotas HTTP (fino, sem lógica de negócio)

tests/                       # testes pytest

scripts/
├── create_database.py       # criação das tabelas
└── import_csv.py            # importação e normalização do CSV

data/
└── Movielist.csv            # dataset de origem

ai/                          # registro do uso de IA no desenvolvimento
```

Regras de arquitetura e desenvolvimento em [CLAUDE.md](CLAUDE.md).

## Status do projeto

### Concluído

* [x] Estrutura inicial do projeto
* [x] Configuração do ambiente com `uv`
* [x] Configuração do SQLAlchemy
* [x] Modelagem da tabela `movies`
* [x] Schemas Pydantic para os dados de filmes
* [x] Criação do banco SQLite
* [x] Importação do dataset `Movielist.csv`
* [x] Normalização dos dados durante a importação
* [x] Conversão de `winner` para booleano

  * `yes` → `True`
  * valor vazio → `False`
* [x] Normalização dos estúdios para lista de strings
* [x] Estrutura para registro do uso de IA no desenvolvimento
* [x] Configuração dos routers da API
* [x] Endpoint para criação de filmes (`POST /movies/`)
* [x] Endpoint para listagem de filmes (`GET /movies/`)
* [x] Endpoint para consulta de um filme por id (`GET /movies/{movie_id}`)
* [x] Endpoint para atualização completa de filmes (`PUT /movies/{movie_id}`)
* [x] Endpoint para atualização parcial de filmes (`PATCH /movies/{movie_id}`)
* [x] Endpoint para remoção de filmes (`DELETE /movies/{movie_id}`)
* [x] Uso de `201 Created` para criação de filmes
* [x] Uso de `204 No Content` para remoção de filmes
* [x] Validação de recurso inexistente com resposta HTTP `404`
* [x] Implementação inicial da lógica de cálculo dos intervalos entre prêmios
* [x] Identificação do maior intervalo entre prêmios consecutivos
* [x] Identificação do menor intervalo entre prêmios consecutivos
* [x] Tratamento de múltiplos produtores por filme
* [x] Tratamento de empate nos maiores e menores intervalos
* [x] Teste preliminar da regra de negócio de intervalos
* [x] Ampliar os testes automatizados das regras de negócio (empate,
  múltiplos produtores, produtor com único prêmio, filmes não vencedores)
* [x] Testes de integração com banco de dados (SQLite isolado em memória,
  sem afetar `movies.db`)
* [x] Testes automatizados dos endpoints da API (CRUD e códigos HTTP
  200/201/204/404/422)
* [x] Validar a lógica de intervalos utilizando o dataset completo
* [x] Endpoint de cálculo dos intervalos integrado à API
  (`GET /movies/producers/awards`)
* [x] Documentação final da API (README com passo a passo de execução,
  testes e lista de endpoints; Swagger em `/docs`)

### Em desenvolvimento

Nenhum item pendente no momento. Novas funcionalidades só serão
adicionadas se especificadas em [SPECS.md](SPECS.md).

## Como rodar

Pré-requisito: Python 3.12 e [uv](https://docs.astral.sh/uv/) instalados.

1. Instalar dependências:

   ```bash
   uv sync
   ```

2. Criar o banco de dados (gera `movies.db` a partir dos modelos):

   ```bash
   uv run python -m scripts.create_database
   ```

3. Importar o dataset `data/Movielist.csv` para o banco:

   ```bash
   uv run python -m scripts.import_csv
   ```

4. Subir a API em modo desenvolvimento:

   ```bash
   uv run uvicorn app.main:app --reload
   ```

5. Acessar a documentação interativa (Swagger):

   http://127.0.0.1:8000/docs

## Endpoints

Atualmente, a API possui as seguintes operações:

| Método   | Endpoint                     | Status de sucesso | Descrição                                                        |
| -------- | ----------------------------- | ----------------- | ----------------------------------------------------------------- |
| `GET`    | `/movies/`                    | `200 OK`          | Lista os filmes cadastrados                                       |
| `GET`    | `/movies/{movie_id}`          | `200 OK`          | Consulta um filme pelo id                                         |
| `GET`    | `/movies/producers/awards`    | `200 OK`          | Retorna os produtores com o maior e o menor intervalo entre vitórias consecutivas |
| `POST`   | `/movies/`                    | `201 Created`     | Cria um novo filme                                                |
| `PUT`    | `/movies/{movie_id}`          | `200 OK`          | Atualiza um filme (substituição completa)                        |
| `PATCH`  | `/movies/{movie_id}`          | `200 OK`          | Atualiza parcialmente um filme                                    |
| `DELETE` | `/movies/{movie_id}`          | `204 No Content`  | Remove um filme                                                   |

Recursos inexistentes (`GET`/`PUT`/`PATCH`/`DELETE` por `movie_id` que não existe) retornam `404 Not Found`.

Dados inválidos enviados à API são validados pelo FastAPI/Pydantic e resultam em `422 Unprocessable Entity`.

A documentação interativa e os schemas das requisições e respostas podem ser consultados pelo Swagger em `/docs`.

## Testes

O projeto tem três níveis de teste:

* **Unitários** (`tests/test_producer_awards.py`, `tests/test_import_csv.py`)
  — cobrem a regra de cálculo dos intervalos por produtor (maior/menor
  intervalo, empate, múltiplos produtores por filme, produtor com um único
  prêmio, filmes não vencedores) e a normalização do CSV, sem tocar banco
  de dados.
* **Integração da API** (`tests/test_movies.py`) — exercitam os fluxos CRUD
  dos endpoints via `TestClient`, validando os status HTTP esperados
  (`200`, `201`, `204`, `404`, `422`) e o endpoint de intervalos
  (`GET /movies/producers/awards`) integrado a FastAPI + SQLAlchemy + banco.
* **Integração com o dataset real** (`tests/test_producer_awards_dataset.py`)
  — carrega `data/Movielist.csv` por completo em um banco de teste isolado
  e valida o resultado final do endpoint de intervalos contra o esperado
  em [SPECS.md](SPECS.md).

Os testes de integração usam um banco SQLite **isolado em memória**
(`tests/conftest.py`), nunca o `movies.db` de desenvolvimento — cada teste
sobe seu próprio banco, populado e descartado ao final. Por isso os testes
podem ser executados a qualquer momento, mesmo com a API rodando, sem
risco de alterar os dados reais.

Para rodar os testes:

1. Instalar as dependências (inclui `pytest` e `httpx`, usados apenas em
   desenvolvimento):

   ```bash
   uv sync
   ```

2. Executar toda a suíte:

   ```bash
   uv run pytest
   ```

   Ou, para ver cada teste individualmente:

   ```bash
   uv run pytest -v
   ```

## Banco de dados

O projeto utiliza SQLite para persistência dos dados.

O banco é criado localmente como:

```text
movies.db
```

Para visualizar os dados pelo SQLite:

```bash
sqlite3 movies.db
```

Exemplo:

```sql
.headers on
.mode column

SELECT * FROM movies LIMIT 10;
```

O campo `winner` é armazenado como booleano. No SQLite, `True` é representado internamente como `1` e `False` como `0`.

## Documentação

* [SPECS.md](SPECS.md) — requisitos conhecidos do teste e o que falta implementar.
* [CLAUDE.md](CLAUDE.md) — contexto do projeto e regras de desenvolvimento.
* [ai/](ai/) — registro do uso de IA no desenvolvimento deste projeto.
