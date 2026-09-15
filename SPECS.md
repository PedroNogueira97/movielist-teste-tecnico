# SPECS.md

Requisitos conhecidos do teste técnico. Este documento é a fonte de
verdade de escopo — ver regra correspondente em [CLAUDE.md](CLAUDE.md).

## Objetivo

Disponibilizar, via API REST, os dados de indicados e vencedores da
categoria **Pior Filme** do Golden Raspberry Awards, permitindo identificar
o(s) produtor(es) com o **maior** e o **menor** intervalo entre dois
prêmios consecutivos.

## Dados de entrada

- Arquivo `data/movies.csv`, carregado em banco (SQLite) na inicialização
  da aplicação.
- Colunas esperadas (a confirmar contra o CSV real quando disponível):
  `year`, `title`, `studios`, `producers`, `winner`.
- O campo `producers` pode conter múltiplos nomes separados por vírgula
  e/ou " and ", exigindo normalização antes do cálculo dos intervalos.
- `winner` indica se o filme venceu o prêmio no ano (apenas filmes
  vencedores entram no cálculo de intervalo).

## Endpoint principal (formato conhecido do teste)

`GET /movies/max-min-win-interval` (nome de rota a confirmar/ajustar na
implementação)

Resposta esperada:

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
  teste).
- Aplicação deve subir e responder sem passos manuais além de
  instalar dependências e rodar o servidor.
- Testes automatizados (pytest) devem validar o resultado do endpoint
  principal contra o dataset fornecido.

## Em aberto / a confirmar

- CSV real do dataset (`data/movies.csv` está vazio, aguardando arquivo
  oficial do teste).
- Nome definitivo da rota e eventuais rotas adicionais (listagem de
  filmes, filtros, paginação) — só serão adicionadas se especificadas.
- Separador e encoding exatos do CSV (o formato usual deste teste usa
  `;` como separador).

## O que ainda precisa ser implementado

Nada de lógica de negócio foi implementado ainda. Pendente:

- [ ] Modelo SQLAlchemy de filme (`app/models/movie.py`)
- [ ] Configuração de engine/sessão (`app/database.py`)
- [ ] Script de importação do CSV (`scripts/import_csv.py`)
- [ ] Schemas Pydantic de entrada/saída (`app/schemas/movie.py`)
- [ ] Serviço de cálculo de intervalos por produtor
      (`app/services/producer_awards.py`)
- [ ] Rota(s) da API (`app/api/routes/movies.py`) e registro em
      `app/main.py`
- [ ] Testes da lógica de negócio (`tests/test_producer_awards.py`)
- [ ] Testes da API (`tests/test_movies.py`)
