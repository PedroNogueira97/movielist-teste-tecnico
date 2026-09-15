# Golden Raspberry Awards API

Teste técnico: API REST em FastAPI para consultar a lista de indicados e vencedores da categoria **Pior Filme** do Golden Raspberry Awards e identificar o(s) produtor(es) com o **maior** e o **menor** intervalo entre dois prêmios consecutivos.

> Projeto em desenvolvimento. A estrutura da aplicação, persistência dos dados, importação do dataset, operações CRUD da API e a primeira implementação da lógica de cálculo dos intervalos já estão implementadas. Os testes das regras de negócio estão sendo desenvolvidos de forma preliminar antes da integração completa com banco de dados e API. Detalhes de escopo em [SPECS.md](SPECS.md).

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
* [x] Uso de `201 Created` para criação de filmes
* [x] Uso de `204 No Content` para remoção de filmes
* [x] Validação de recurso inexistente com resposta HTTP `404`
* [x] Implementação inicial da lógica de cálculo dos intervalos entre prêmios
* [x] Identificação do maior intervalo entre prêmios consecutivos
* [x] Identificação do menor intervalo entre prêmios consecutivos
* [x] Tratamento de múltiplos produtores por filme
* [x] Tratamento de empate nos maiores e menores intervalos
* [x] Teste preliminar da regra de negócio de intervalos

### Em desenvolvimento

* [ ] Ampliar os testes automatizados das regras de negócio
* [ ] Testes de integração com banco de dados
* [ ] Testes automatizados dos endpoints da API
* [ ] Validar a lógica de intervalos utilizando o dataset completo
* [ ] Finalizar a integração da lógica de intervalos com a API
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

| Método   | Endpoint             | Status de sucesso | Descrição                      |
| -------- | -------------------- | ----------------- | ------------------------------ |
| `GET`    | `/movies/`           | `200 OK`          | Lista os filmes cadastrados    |
| `POST`   | `/movies/`           | `201 Created`     | Cria um novo filme             |
| `PUT`    | `/movies/{movie_id}` | `200 OK`          | Atualiza um filme              |
| `PATCH`  | `/movies/{movie_id}` | `200 OK`          | Atualiza parcialmente um filme |
| `DELETE` | `/movies/{movie_id}` | `204 No Content`  | Remove um filme                |

Recursos inexistentes retornam `404 Not Found`.

Dados inválidos enviados à API são validados pelo FastAPI/Pydantic e podem resultar em `422 Unprocessable Entity`.

A documentação interativa e os schemas das requisições e respostas podem ser consultados pelo Swagger em `/docs`.

## Testes

Os testes estão sendo implementados de forma incremental.

Neste momento, foram criados **testes preliminares das regras de negócio**, isolando a lógica de cálculo dos intervalos antes de integrá-la diretamente ao banco de dados e aos endpoints da API.

Essa abordagem permite validar primeiro a regra de negócio de forma isolada e, posteriormente, adicionar os testes de integração e da API.

Executar os testes:

```bash
uv run pytest
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
