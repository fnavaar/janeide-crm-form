# Fase 1 — Captura e painel mínimo

> Estado resumido da fase. Detalhes operacionais nos contratos e SPECs.

## Progresso

- Tasks: **7/16 concluídas** (F1-T01 a F1-T07); F1-T08 em próximo.
- Levas: leva 1 (contratos) 100% fechada; levas 2–4 do caminho principal concluídas; leva 5 (F1-T08) próxima.

## Entregas recentes

- **F1-T05** — captura idempotente (webhook WhatsApp/Meta, dedupe, opt-out). Concluída e aprovada.
- **F1-T06** — fila de leads + cartão mínimo + próximo passo + auditoria. Concluída e aprovada.
- **F1-T07** — catálogo mínimo (properties) + consulta por código + preview de ficha com bloqueio por vigência/status. **Concluída e aprovada** (preview CASAS-TURIM-001 com fonte/vigência; bloqueios INATIVO/VENCIDO; nenhum dado inventado).

## Pendências e riscos

- Rotação da senha SDR (secret `SDR_TEST_CREDENTIALS`).
- Trocar `META_APP_SECRET` de teste pelo real antes de publicar.

## Como consultar

- Estado executivo: `STATUS.md`
- Histórico: `changelog.md`
- SPECs desta fase: `04_fase-atual/specs/`
