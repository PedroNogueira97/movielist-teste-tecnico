# Golden Raspberry Awards API

Teste técnico: API REST em FastAPI para consultar a lista de indicados e vencedores da categoria **Pior Filme** do Golden Raspberry Awards e identificar o(s) produtor(es) com o **maior** e o **menor** intervalo entre dois prêmios consecutivos.

> Projeto em desenvolvimento. A estrutura da aplicação, persistência dos dados, importação do dataset e operações CRUD da API já estão implementadas. A lógica de negócio para cálculo dos intervalos entre prêmios ainda está em desenvolvimento. Detalhes de escopo em [SPECS.md](SPECS.md).

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
* [x] Endpoint para consulta de filmes (`GET /movies/`)
* [x] Endpoint para atualização completa de filmes (`PUT /movies/{movie_id}`)
* [x] Endpoint para atualização parcial de filmes (`PATCH /movies/{movie_id}`)
* [x] Endpoint para remoção de filmes (`DELETE /movies/{movie_id}`)
* [x] Validação de recurso inexistente com resposta HTTP `404`
* [x] Testes manuais dos endpoints CRUD via Swagger

### Em desenvolvimento

* [ ] Implementação da lógica para identificar maior intervalo entre prêmios
* [ ] Implementação da lógica para identificar menor intervalo entre prêmios
* [ ] Testes automatizados da API e das regras de negócio
* [ ] Documentação final da API

## Como rodar

Instalar dependências:

```bash
uv sync
```

Criar o banco de dados:

```bash
uv run python -m scripts.create_database
```

Importar o dataset:

```bash
uv run python -m scripts.import_csv
```

Subir a API em modo desenvolvimento:

```bash
uv run uvicorn app.main:app --reload
```

Docs interativas (Swagger):

http://127.0.0.1:8000/docs

## Endpoints

Atualmente, a API possui as seguintes operações:

| Método   | Endpoint             | Descrição                      |
| -------- | -------------------- | ------------------------------ |
| `GET`    | `/movies/`           | Lista os filmes cadastrados    |
| `POST`   | `/movies/`           | Cria um novo filme             |
| `PUT`    | `/movies/{movie_id}` | Atualiza um filme              |
| `PATCH`  | `/movies/{movie_id}` | Atualiza parcialmente um filme |
| `DELETE` | `/movies/{movie_id}` | Remove um filme                |

A documentação interativa e os schemas das requisições e respostas podem ser consultados pelo Swagger em `/docs`.

## Testes

```bash
uv run pytest
```

Os testes automatizados das rotas e das regras de negócio ainda estão em desenvolvimento.

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
