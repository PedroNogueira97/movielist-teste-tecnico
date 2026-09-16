# ai/

Esta pasta documenta o uso de IA no desenvolvimento deste projeto: o que foi
pedido, o que foi gerado, o que foi revisado/ajustado e como foi validado.
O objetivo é dar transparência ao processo, sem guardar dumps completos de
conversas.

## Ferramentas de IA utilizadas

- **Claude Code** (Anthropic) — assistente de codificação usado para
  estruturar o projeto, implementar funcionalidades e escrever testes.

## Organização

- `decisions.md` — decisões técnicas relevantes tomadas com apoio de IA
  (escolhas de arquitetura, formato de dados, bibliotecas), em formato
  curto: decisão + motivo.
- `prompts/` — um registro por tarefa relevante concluída com auxílio de
  IA, numerado sequencialmente (`001-slug.md`, `002-slug.md`, ...).
  Cada registro segue o template descrito na skill `document-ai`
  (`.claude/skills/document-ai/SKILL.md`) e contém: objetivo, prompt
  utilizado, resultado produzido, revisão/decisões, problemas encontrados
  e validação realizada.

## Registros existentes

- [001 - Estrutura inicial do projeto](prompts/001-project-structure.md)
- [002 - Suíte de testes (unitários, integração de API e dataset real)](prompts/002-test-suite.md)
