# AP-2026-09-28-1620 — valores zero/false em campos PocketBase

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T02 / SPEC-2-001
- Sinal: no runtime PocketBase v0.36 do Skip 55154, `stale_review: false` foi rejeitado como `cannot be blank` quando o booleano era `required: true`. Em seguida, a resposta original foi mascarada porque o recibo de falha enviou `accepted=0` e `pending=0` a campos numéricos obrigatórios.
- Evidência: migrations `0028_f2_t02_allow_zero_counts.js` e `0029_f2_t02_allow_false_flags.js`; import V1 e suíte runtime 19/19 PASS em 2026-09-28.
- Regra reutilizável: não marcar como obrigatórios campos numéricos/booleanos cujo domínio válido inclui 0/false; preserve a exceção primária separadamente para não mascarar falhas durante a gravação do recibo.
- Quando aplicar: esquema PocketBase v0.36 que precisa persistir zeros/falsos como valores válidos; valide o comportamento no runtime.
- Quando não aplicar: campos onde zero/false realmente significam ausência ou são proibidos pelo contrato de negócio.
- Confiança: alta — causa observada, corrigida por migrations e coberta por import e falha parcial runtime.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
