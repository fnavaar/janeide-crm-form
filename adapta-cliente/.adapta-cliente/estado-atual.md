# Estado atual — Adapta Cliente

- task_id: F1-T08
- champion: Matheus Silva
- spec: 04_fase-atual/specs/spec-fase-1-004-pedido-visita.md
- etapa: concluida
- autorizacao_implementacao: confirmada + 2026-09-03T13:20-03:00 + "Plano da F1-T08 aprovado... Pode implementar."
- teste_humano: aprovado + 2026-09-03T14:46-03:00 + "4º teste aprovado — todos os cenários funcionaram: dedupe corrigido (repetir mesma janela não duplica), máscara de digitação funcionando, 'Precisa esclarecer' confirmado sem alteração. F1-T08 aprovada."
- verificacao_automatica: passou — QA 0.0.35 verde (build/static/integrations/test); dedupe com findRecordsByFilter (lead+imóvel+status não-cancelado); máscara maskWindow no bundle; 401 sem auth nos hooks
- aprendizado: capturado: AP-2026-09-03-1150 (actor.id), AP-2026-09-03-1155 (datetime→RFC3339), AP-2026-09-03-1200 (dedupe ignora cancelado); sem sinal novo no fechamento
- ultima_acao: F1-T08 concluída — fase.md (CONCLUÍDA), STATUS.md (8/16), changelog (conclusão), estado=concluida
- proxima_acao: nenhuma (parar; aguardar pedido para F1-T09)
- atualizado_em: 2026-09-03T14:46-03:00