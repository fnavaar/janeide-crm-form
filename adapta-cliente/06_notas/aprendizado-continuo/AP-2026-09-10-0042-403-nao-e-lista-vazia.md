# AP-2026-09-10-0042 — 403 não é lista vazia

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T14 / SPEC-1-002
- Sinal: corretor sem atribuição recebia uma interface vazia, indistinguível de auditoria sem eventos.
- Evidência: teste humano encontrou a ambiguidade; correção 0.0.59 preservou 403 e mostrou mensagem explícita; lista 200 vazia permaneceu distinta.
- Regra reutilizável: interfaces que exibem coleções protegidas devem diferenciar ausência de dados, acesso negado e falha técnica.
- Quando aplicar: listas de auditoria, pendências e dados filtrados por papel.
- Quando não aplicar: componentes sem controle de acesso ou sem estado de erro distinto.
- Confiança: alta — causa reproduzida, correção automatizada e teste humano aprovados.
- Privacidade: sem segredo, token ou PII
