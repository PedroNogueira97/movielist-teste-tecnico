# Golden Raspberry Awards API

Teste técnico: API REST em FastAPI para consultar a lista de indicados e
vencedores da categoria **Pior Filme** do Golden Raspberry Awards e
identificar o(s) produtor(es) com o **maior** e o **menor** intervalo
entre dois prêmios consecutivos.

> Projeto em fase de estruturação inicial — apenas esqueleto e
> documentação, sem lógica de negócio implementada ainda. Detalhes de
> escopo em [SPECS.md](SPECS.md).

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest
- [uv](https://docs.astral.sh/uv/) (dependências e ambiente)

## Estrutura

```text
app/
├── main.py              # instancia o FastAPI e registra routers
├── database.py          # engine/session do SQLAlchemy
├── models/               # modelos SQLAlchemy (tabelas)
├── schemas/               # schemas Pydantic (entrada/saída da API)
├── services/               # lógica de negócio
└── api/routes/               # rotas HTTP (fino, sem lógica de negócio)

tests/                   # testes pytest
scripts/import_csv.py     # importação do CSV para o banco
data/movies.csv            # dataset de origem
ai/                       # registro do uso de IA no desenvolvimento
```

Regras de arquitetura e desenvolvimento em [CLAUDE.md](CLAUDE.md).

## Como rodar

Instalar dependências:

```bash
uv sync
```

Subir a API em modo desenvolvimento:

```bash
uv run uvicorn app.main:app --reload
```

Docs interativas (Swagger): http://127.0.0.1:8000/docs

## Testes

```bash
uv run pytest
```

## Documentação

- [SPECS.md](SPECS.md) — requisitos conhecidos do teste e o que falta
  implementar.
- [CLAUDE.md](CLAUDE.md) — contexto do projeto e regras de
  desenvolvimento.
- [ai/](ai/) — registro do uso de IA no desenvolvimento deste projeto.
