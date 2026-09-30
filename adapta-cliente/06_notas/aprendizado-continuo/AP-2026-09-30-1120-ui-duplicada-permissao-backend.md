# AP-2026-09-30-1120 — UI duplicada e autorização no backend

- Status: capturado (validação humana do cartão único aprovada no fechamento da F2-T02 em 2026-09-30)
- Escopo: projeto do cliente
- Task/SPEC: F2-T02 / SPEC-2-001
- Sinal: dois cartões de mutação renderizados sob a mesma condição de papel geraram controles visuais duplicados, embora ambos chamassem a mesma rota e o backend continuasse negando SDR com HTTP 403.
- Evidência: correção registrada em `06_notas/debug/debug-2026-09-30-f2-t02-duplicated-read-only-card.md`; fonte `src/pages/CatalogoF2T02.tsx`; QA Skip 0.0.76 PASS.
- Regra reutilizável: para ações condicionadas por papel, revisar contagem/visibilidade dos componentes por papel separadamente da autorização do backend; eliminar affordances duplicadas sem remover a verificação server-side, e testar que a tentativa não-admin continua retornando 403.
- Quando aplicar: interfaces com botões de mutação ou controles de teste condicionados por papel.
- Quando não aplicar: quando os cartões diferentes representam explicitamente ações distintas no contrato.
- Confiança: média — causa e correção confirmadas no código e QA; validação humana visual pós-correção ainda pendente.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
