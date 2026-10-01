# AP-2026-10-01-1830 — Gate de leitura deve preservar o smoke do superuser

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T04 / SPEC-2-002 (CA-2-012)
- Sinal: middleware global `routerUse` para restringir leitura de PII de lead por papel recusou a sessão superuser da plataforma com 401; a pipeline Skip detectou o travamento, reverteu o deploy e reportou o erro literal. Um bypass `hasSuperuserAuth()` existia no REST, mas faltava no handler de subscriptions realtime, e a checagem `!e.auth` rodava antes de o middleware reconhecer a rota alvo.
- Evidência: QA 0.0.88 (`cadd8ea`) integrations FAIL com mensagem "Deploy of 'leads_read_role_gate' was reverted…"; correção em 0.0.91 (`085a804`) com bypass explícito em REST e realtime + checagem só após casar a rota `leads`; QA 5/5 PASS. Registro em `06_notas/debug/debug-2026-10-01-f2-t04-role-gate-superuser-smoke.md`.
- Regra reutilizável: em hooks de autorização global no PocketBase/Skip, o bypass de superuser (`e.hasSuperuserAuth()`) deve ser a primeira verificação em TODA superfície registrada (REST e realtime), e qualquer negação de sessão só pode ocorrer depois de o middleware confirmar que a rota é alvo do gate; validar com a pipeline oficial antes de considerar o gate aplicado.
- Quando aplicar: qualquer `routerUse`/middleware global que negue requisição em plataforma gerenciada com smoke automatizado.
- Quando não aplicar: hooks de rota única com `requireAuth` que não interceptam rotas da plataforma.
- Confiança: alta — falha reproduzida pela pipeline, correção verificada por QA 5/5 e leitura de volta dos arquivos.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
