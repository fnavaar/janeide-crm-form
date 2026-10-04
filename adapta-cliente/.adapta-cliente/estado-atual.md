# Estado atual — Adapta Cliente

- task_id: F2-T07
- champion: Matheus Silva
- spec: 04_fase-atual/specs/spec-fase-2-004-atendimento-prioridade-handoff.md
- etapa: em_correcao
- autorizacao_implementacao: confirmada por Janeide em 2026-10-02 12:05 ("Autorizo implementar a F2-T07 conforme este plano.")
- teste_humano: pendente
- verificacao_automatica: pendente — nenhuma build/QA da implementação F2-T07 executada; projeto Skip 55154 segue no preview 0.0.96 (`4cdd865`), sem publicação; migration 0033 pendente.
- aprendizado: pendente
- ultima_acao: Candidato de `Index.tsx` reconstruído localmente a partir do baseline 0.0.96 (SHA-256 `0d0682102579966075f307b144a199008dd9cf01ec43b85dadb6845976e0a338`) e diff completo revisado: SHA-256 do candidato `6dc64b5e3bccbc6ea28893de318f5a76c8d16a40a07f191f7e5d52a8a61c66e7`; visitas F1, auditoria e `ClickUpField` conferidos byte a byte contra o baseline. Proposta de escrita futura: `skip_file_patch` com 3 blocos SEARCH/REPLACE, ainda não executada e aguardando aval separado de Janeide. Nenhuma gravação no Skip, build, QA ou migration nesta etapa.
- proxima_acao: aguardar aval explícito de Janeide para executar uma única chamada `skip_file_patch`; depois reler `Index.tsx` e aceitar somente se o hash do readback for idêntico ao candidato; se divergir, parar sem nova tentativa.
- atualizado_em: 2026-10-04T18:23:50-03:00
