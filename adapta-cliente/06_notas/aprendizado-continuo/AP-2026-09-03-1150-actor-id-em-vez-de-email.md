# AP-2026-09-03-1150-actor-id-em-vez-de-email

- Status: candidato
- Escopo: projeto do cliente (Skip Cloud, hooks JS)
- Task/SPEC: F1-T08 / SPEC-1-004
- Sinal: ao gravar `created_by: actor.email || actor.id` no hook `visita/registrar`, o request falhou com `created_by: cannot be blank` (status 0). O auth record do usuário SDR (`sdr@janeide.test`) **não tem o campo `email` populado no registro** (só o login), então `actor.email` é `''` e, sem fallback em `actor.id` (que o PocketBase sempre preenche), o campo required ficou vazio. Mesmo padrão em `cancelled_by` no hook de cancelar.
- Regra reutilizável: ao registrar ator em hooks da Skip, usar **`actor.id || actor.email || ''`** (id primeiro — sempre presente). `actor.email` NÃO é confiável no auth record de usuários criados via `setEmail` (o email pode não estar exposto no registro). Além disso, mensagens de erro genéricas no frontend ("Falha ao registrar...") mascaram a causa real — sempre consultar os logs do servidor antes de presumir regra de negócio.
- Quando aplicar: toda escrita de `created_by`/`cancelled_by`/`actor` em hooks; todo debug de erro genérico no painel.
- Quando não aplicar: não se aplica a quem usa o email explicitamente (ex.: e-mail do lead).
- Confiança: alta — erro reproduzido 3x nos logs, corrigido com `actor.id` (deploy 0.0.32), QA verde.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.