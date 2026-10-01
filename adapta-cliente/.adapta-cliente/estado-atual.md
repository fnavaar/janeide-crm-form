# Estado atual — Adapta Cliente

- task_id: F2-T04
- champion: Matheus Silva
- spec: 04_fase-atual/specs/spec-fase-2-002-busca-ficha-vigente.md
- etapa: concluida
- autorizacao_implementacao: confirmada por Janeide em 2026-10-01 15:28 ("pode terminar: aplicar o middleware e a migration 0032, rodar a pipeline, e validar 403 para role=outro + leitura normal para os papéis permitidos")
- teste_humano: aprovado por Janeide em 2026-10-01 20:10 ("Testei e funcionou. Confirmo: A1 ✓, A2 ✓, B1 ✓, B2 ✓, C1 ✓ (outro bloqueado com 403 nos dois endpoints), C2 ✓ (SDR, Corretor e Admin leem normalmente, 200 em listagem e cartão). A3 permanece como pendência registrada")
- verificacao_automatica: passou — Skip 55154 0.0.91 (`085a804`) setup/static/build/integrations/test 5/5 PASS; migration 0032 aplicada; RLS `leads` allowlist admin/sdr/corretor confirmada por leitura de volta; middleware com bypass superuser em REST e realtime; anônimo 401 (host interno); sonda e probe key removidos e confirmados.
- aprendizado: capturado:06_notas/aprendizado-continuo/AP-2026-10-01-1830-superuser-smoke-em-gate-global.md + AP-2026-10-01-1835-placeholder-em-roteiro-humano.md
- ultima_acao: fechamento formal da F2-T04 — fase.md 4/8, STATUS, changelog, aprendizados capturados, estado concluida; sincronização GitHub executada em partes via MCP.
- proxima_acao: aguardar autorização explícita de Janeide para iniciar F2-T05.
- atualizado_em: 2026-10-01T20:55:00-03:00
