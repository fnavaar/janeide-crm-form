# AP-2026-10-01-1835 — Placeholder de teste humano gera 404 falso-positivo

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T04 / SPEC-2-002 (CA-2-012)
- Sinal: roteiro humano usou `LEAD-TESTE-001` como exemplo de `lead_id`; o hook do cartão buscou pelo campo real e retornou 404 "lead not found", confundindo a validadora entre ID inexistente, falta de permissão (403) e ausência de token (401).
- Evidência: relato de Janeide no teste C2 (listagem 200, cartão 404); código de `pocketbase/hooks/acesso.js` busca por `lead_id`; roteiro corrigido para instruir copiar `lead_id` da listagem e distinguir 403/401/404.
- Regra reutilizável: roteiro de teste humano deve instruir a copiar identificadores reais da própria resposta anterior da API (ex.: `lead_id` da listagem), nunca placeholders; e deve incluir um mini-guia de códigos HTTP (401 vs 403 vs 404) para o resultado ser interpretável sem a assistente.
- Quando aplicar: roteiros de teste humano que encadeiam chamadas dependentes em APIs com autenticação por papel.
- Quando não aplicar: provas totalmente automatizadas onde a assistente controla os identificadores.
- Confiança: alta — causa confirmada pela diferença 403 (C1) vs 404 (C2) no mesmo endpoint.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
