# SPECs da Fase 2 — Imobiliária Janeide Xavier

**Fase:** 2 — Sistematizar catálogo e atendimento consultivo  
**Estado:** revisadas e preparadas para execução task a task  
**Fonte:** escopo definitivo, matriz de rastreabilidade, contratos e provas da Fase 1

## Resultado da fase

O SDR atende no painel, encontra imóveis por código, bairro ou tipo, revisa uma ficha proveniente do catálogo mínimo vigente, registra o envio humano e mantém histórico, prioridade, exceção e próximo passo sem abandonar o contexto do lead.

## SPECs

| Ordem | SPEC | Resultado observável | Estado inicial |
|---:|---|---|---|
| 1 | [SPEC-2-001 — Catálogo mínimo, carga e vigência](spec-fase-2-001-catalogo-carga-vigencia.md) | lote validado, versionado e reconciliável | planejada; B2-01/B2-02 |
| 2 | [SPEC-2-002 — Busca consultiva e ficha vigente](spec-fase-2-002-busca-ficha-vigente.md) | busca por código/bairro/tipo | bloqueada por SPEC-2-001 |
| 3 | [SPEC-2-003 — Card e envio humano rastreável](spec-fase-2-003-card-envio-humano.md) | card e registro de envio manual | bloqueada por SPEC-2-001/002 |
| 4 | [SPEC-2-004 — Atendimento consultivo, prioridade e próximo passo](spec-fase-2-004-atendimento-prioridade-handoff.md) | contexto, exceção e handoff auditável | bloqueada por SPEC-2-002/003 e B2-08 |

## Bloqueios

- **B2-01:** amostra/layout da exportação Kenlo.
- **B2-02:** data de corte, vigência e responsável.
- **B2-03:** acesso ao Skip ou evidência exportável.
- **B2-04:** política de retenção/log/PII.
- **B2-05:** ICP e prioridade; bloqueia classificação produtiva, não a fila.
- **B2-06:** `message_ref` pode não existir; usar recibo manual explícito.
- **B2-08:** matriz de acesso e contrato de handoff.

## Cobertura

SPEC-2-001: CA-2-001..006 · SPEC-2-002: CA-2-007..012 · SPEC-2-003: CA-2-013..018 · SPEC-2-004: CA-2-019..024.

F2-T01..T08 estão em `fase.md`; somente F2-T01 é elegível.
