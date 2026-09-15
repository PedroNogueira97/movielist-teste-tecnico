# CLAUDE.md

Contexto e regras de desenvolvimento para este projeto. Leia antes de gerar
ou alterar código.

## Contexto do projeto

Teste técnico: API REST em FastAPI para consultar a lista de indicados e
vencedores da categoria **Pior Filme** do Golden Raspberry Awards, a partir
de um CSV (`data/movies.csv`), calculando os produtores com o **menor** e o
**maior** intervalo entre dois prêmios consecutivos. Detalhes em [SPECS.md](SPECS.md).

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest
- uv (gerenciamento de dependências e ambiente)

## Estrutura

```text
app/
├── main.py                  # instancia o FastAPI e registra routers
├── database.py               # engine/session do SQLAlchemy
├── models/                   # modelos SQLAlchemy (tabelas)
├── schemas/                  # schemas Pydantic (entrada/saída da API)
├── services/                 # lógica de negócio
└── api/routes/                # rotas HTTP (fino, sem lógica de negócio)

tests/                        # testes pytest
scripts/import_csv.py          # importação do CSV para o banco
data/movies.csv                 # dataset de origem
ai/                            # registro do uso de IA no desenvolvimento
```

## Regras de desenvolvimento

- Manter a arquitetura simples: sem DDD, sem Clean Architecture, sem
  camadas ou abstrações que a estrutura acima não exige.
- Não adicionar abstrações (interfaces, factories, repositórios genéricos
  etc.) sem necessidade concreta e imediata.
- Lógica de negócio vive em `app/services/`. Rotas (`app/api/routes/`)
  apenas recebem a requisição, chamam o service e devolvem a resposta.
- Acesso ao banco de dados fica isolado (`app/database.py` e `app/models/`)
  e não é misturado com o código das rotas.
- Usar type hints em todas as funções e métodos.
- Escrever testes (pytest) para a lógica de negócio, especialmente o
  cálculo dos intervalos de prêmios por produtor.
- Não adicionar dependências além das listadas no stack acima sem
  necessidade justificada.
- Seguir PEP 8.
- Não implementar funcionalidades que não estejam especificadas em
  [SPECS.md](SPECS.md). Em caso de dúvida sobre escopo, perguntar antes de
  implementar.

## Uso de IA

Tarefas relevantes concluídas com auxílio de IA devem ser registradas
usando a skill `document-ai` (`.claude/skills/document-ai/SKILL.md`), que
mantém o histórico em `ai/`.
