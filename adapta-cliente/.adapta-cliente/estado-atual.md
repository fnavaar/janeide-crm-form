# Estado atual — Adapta Cliente

- task_id: F1-T09
- champion: Matheus Silva
- spec: 04_fase-atual/specs/spec-fase-1-001-captura-lead-origem.md
- etapa: concluida
- autorizacao_implementacao: confirmada + 2026-09-03T14:58-03:00 + "Plano aprovado — pode implementar as duas correções..."
- teste_humano: aprovado + 2026-09-04T12:53-03:00 + "Todos os 5 cenários passaram exatamente como esperado: 400 source_channel inválido; 200 pending invalid_property_code sem criar lead; 201 created / 200 duplicate (mesmo lead_id); 200 rejected opt-out. F1-T09 aprovada."
- verificacao_automatica: passou — QA 0.0.36 verde; 5 cenários executados via curl com assinatura pré-calculada (secret de teste definido pelo agente); 401 pré-assinatura confirmados
- aprendizado: capturado:AP-2026-09-04-1200-hmac-gerado-com-python (assinatura webhook) — pendente publicação GitHub
- ultima_acao: F1-T09 concluída — fase.md (CONCLUÍDA), STATUS.md (9/16), changelog (conclusão), estado=concluida
- pendencia_aberta: META_APP_SECRET rotacionado 2026-09-04 (valor de teste desativado, 401 confirmado; novo valor só do usuário, validado sem ver). Resta trocar pelo App Secret real da Meta antes de produção.
- proxima_acao: aguardar pedido para F1-T10
- atualizado_em: 2026-09-04T14:01-03:00