# AP-2026-09-09-0015 — Secret temporário de demonstração deve rotacionar

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T13 / SPEC-1-001
- Sinal: demonstração de webhook exige assinatura HMAC, mas o secret temporário de teste não pode permanecer configurado após a prova.
- Evidência: `cap-demo-f1t13` retornou 201 created; reenvio de `cap-001` retornou 200 duplicate; handoff foi confirmado no painel; META_APP_SECRET temporário permaneceu no Skip Cloud ao final da rodada.
- Regra reutilizável: qualquer secret temporário usado para teste deve ter rotação explícita antes de produção ou da próxima task que dependa do ambiente.
- Quando aplicar: testes de webhook HMAC e integrações com credencial configurada em runtime.
- Quando não aplicar: quando o teste usa um secret definitivo já escolhido pelo proprietário e não exposto ao agente.
- Confiança: alta — respostas do webhook, logs e aceite humano confirmados.
- Privacidade: sem segredo, token ou PII
