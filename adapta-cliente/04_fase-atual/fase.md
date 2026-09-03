# Fase 1 — Captura e painel mínimo

> Estado resumido da fase. Detalhes operacionais nos contratos e SPECs.

## Progresso

- Tasks: **6/16 concluídas** (F1-T01 a F1-T06); F1-T07 em implementação.
- Levas: leva 1 (contratos) 100% fechada; leva 2 (implementação) em andamento.

## Entregas recentes

- **F1-T05** — captura idempotente (webhook WhatsApp/Meta, dedupe, opt-out). Concluída e aprovada.
- **F1-T06** — fila de leads + cartão mínimo + próximo passo + auditoria. Concluída e aprovada.
- **F1-T07** — catálogo mínimo (properties) + consulta por código + preview de ficha com bloqueio por vigência/status. Implementada; em teste humano.

## Pendências e riscos

- Teste humano da F1-T07 (2ª tentativa) — 1º falhou com erro técnico (ReferenceError no hook), corrigido.
- Rotação da senha SDR (secret `SDR_TEST_CREDENTIALS`).
- Trocar `META_APP_SECRET` de teste pelo real antes de publicar.

## Como consultar

- Estado executivo: `STATUS.md`
- Histórico: `changelog.md`
- SPECs desta fase: `04_fase-atual/specs/`
