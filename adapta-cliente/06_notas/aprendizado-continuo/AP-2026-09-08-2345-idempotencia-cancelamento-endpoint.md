# AP-2026-09-08 2345 — Idempotência de cancelamento no endpoint

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T12 / SPEC-1-004
- Sinal: a UI esconde a ação Cancelar depois do status Cancelado, mas isso não prova a idempotência do backend.
- Evidência: teste autenticado da segunda tentativa retornou `already_cancelled`; `cancelled_at` e `cancel_reason` permaneceram iguais e nenhum registro novo foi criado.
- Regra reutilizável: critérios de idempotência devem ser testados diretamente no endpoint autenticado, além da interface; confirmar resposta idempotente e invariantes do registro.
- Quando aplicar: cancelamentos, retries e ações destrutivas idempotentes com ação ocultada após o primeiro sucesso.
- Quando não aplicar: quando a SPEC exigir apenas comportamento visual, sem contrato de idempotência de API.
- Confiança: alta — teste humano e resposta backend confirmados pela owner.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto
