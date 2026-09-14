# AP-2026-09-09-0015 — acesso temporário de demonstração deve ser rotacionado

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T13 / SPEC-1-001
- Sinal: demonstração de webhook exige assinatura, mas o acesso temporário de teste não pode permanecer configurado após a prova.
- Evidência: a demonstração e o reenvio idempotente foram aprovados; a configuração temporária permaneceu no ambiente ao fim da rodada.
- Regra reutilizável: qualquer acesso temporário usado em teste deve ter rotação explícita antes de produção ou da próxima task que dependa do ambiente.
- Quando aplicar: testes de webhook e integrações com acesso configurado em runtime.
- Confiança: alta.
- Privacidade: sem valor de acesso ou PII.
