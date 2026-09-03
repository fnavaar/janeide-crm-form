# AP-2026-09-03-1200-dedupe-deve-ignorar-registros-cancelados

- Status: candidato
- Escopo: projeto do cliente (Skip Cloud, hooks JS / PocketBase)
- Task/SPEC: F1-T08 / SPEC-1-004
- Sinal: a idempotência de pedido de visita (`CA-1-16`) quebrou ao repetir a mesma janela estruturada. Causa: o dedupe usava `findFirstRecordByData('visit_requests', 'lead_id', leadId)` e comparava `status === status`. Como o lead tinha um pedido **cancelado** (status `Cancelado`) e um novo `Pendente de agenda`, o finder retornava o primeiro arbitrário (ou o cancelado), a comparação de status falhava e o sistema criava um segundo pedido. Com texto livre funcionava porque só havia um pedido.
- Regra reutilizável: **nunca** deduplicar por chave parcial (`lead_id`) com `findFirstRecordByData` quando pode haver múltiplos registros ou registros em estados que devem ser ignorados. Usar `findRecordsByFilter('col', 'a = {:x} && b = {:y} && status = {:s}', '-created', 1, 0, params)` filtrando os estados relevantes (ex.: ignorar `Cancelado`). Para idempotência, filtrar exatamente o "estado ativo" que define a duplicata.
- Quando aplicar: toda checagem de duplicidade em coleções com estados (pedidos, eventos, transações).
- Quando não aplicar: coleções onde a chave é única e sem estados (ex.: `capture_event_id`).
- Confiança: alta — bug reproduzido no teste humano (2 pedidos criados), corrigido com filtro completo (deploy 0.0.35), QA verde.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.