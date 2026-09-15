---
name: document-ai
description: Registra em ai/ o uso de IA neste projeto sempre que uma tarefa relevante for concluída com auxílio da IA (nova funcionalidade, decisão de arquitetura, correção de bug não trivial, etc). Use ao final de uma tarefa relevante, não para cada pequena interação.
---

# document-ai

Documenta, de forma resumida e legível, tarefas relevantes concluídas com
ajuda de IA neste projeto. O objetivo é dar visibilidade ao processo de
desenvolvimento assistido por IA, não arquivar a conversa inteira.

## Quando usar

Ao final de uma tarefa relevante concluída com auxílio de IA. Exemplos:
implementar uma funcionalidade, tomar uma decisão de arquitetura,
corrigir um bug não trivial, criar/alterar estrutura do projeto.

Não usar para cada mensagem trocada ou ajuste trivial (ex.: corrigir um
typo, renomear uma variável).

## O que fazer

1. Verifique o próximo número disponível em `ai/prompts/` (arquivos são
   `NNN-slug-curto.md`, com `NNN` sequencial e zero-padded, ex.: `001`,
   `002`).
2. Crie `ai/prompts/NNN-slug-curto.md` com o registro da tarefa, usando o
   template abaixo. O slug deve ser curto e descritivo (kebab-case),
   coerente com a tarefa (ex.: `csv-import`, `producer-intervals`).
3. Se a tarefa envolveu uma decisão técnica não óbvia (escolha de
   biblioteca, formato de dados, estratégia de cálculo, etc.), registre-a
   também em `ai/decisions.md` (formato livre e curto: decisão + motivo).
4. Atualize `ai/README.md` se necessário: adicione o novo registro à
   lista de registros existentes e/ou atualize a lista de
   ferramentas/skills de IA usadas no projeto, caso tenha mudado.

## Template do registro (`ai/prompts/NNN-slug-curto.md`)

Seja objetivo. Cada seção deve ter poucas linhas — isto não é um dump da
conversa.

```markdown
# NNN - Título curto da tarefa

## Objetivo

O que a tarefa buscava resolver/entregar, em 1-3 frases.

## Prompt utilizado

Cole aqui o prompt original do usuário **literalmente, na íntegra**
(verbatim, sem resumir e sem parafrasear).

## Resultado produzido pela IA

O que foi gerado/alterado, em bullets (arquivos, endpoints, funções).

## Revisão e decisões técnicas

Ajustes feitos sobre o resultado da IA e por quê. Omitir a seção se não
houve decisão relevante além de aceitar o resultado.

## Problemas encontrados e correções

Erros, comportamentos inesperados ou retrabalho e como foram corrigidos.
Omitir a seção se não houve problemas.

## Validação

Como o resultado foi validado: testes executados (`pytest ...`), comandos
rodados, verificação manual, etc.
```

## Regras

- O "Prompt utilizado" é a exceção à concisão: é sempre o prompt original
  do usuário colado literalmente, mesmo que longo.
- Nas demais seções, não copiar a conversa inteira nem trechos longos de
  código no registro — referencie arquivos/caminhos, o código já está no
  repositório. Não é para incluir a saída completa de comandos, apenas os
  pontos relevantes.
- Manter cada registro curto (o objetivo é legibilidade, não completude
  arquivística).
- Numeração é sequencial e nunca reaproveitada, mesmo que uma tarefa seja
  descartada depois.
- Um registro por tarefa concluída, não por sessão de chat.
