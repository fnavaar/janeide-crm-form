# AP-2026-10-02-0845 — login do painel de teste só no host interno do backend

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T06 / SPEC-2-003 (prova de regressão)
- Sinal: no teste humano, o login via curl retornou 405 Not Allowed (nginx) quando feito no host do preview (`--preview.goskip.app`); o endpoint `/api/collections/users/auth-with-password` só funciona no host interno do backend (`shrd00.internal.goskip.dev`). O mesmo já ocorrera com rotas `/backend/*` (200 falso por fallback SPA no preview).
- Evidência: testes curl comparativos (POST no interno = 400/200; POST no preview = 405); logs Skip 55154 com login 200 no interno; relato de Janeide no início da F2-T06.
- Regra reutilizável: roteiros de teste humano no Skip 55154 devem usar SEMPRE o host interno do backend para qualquer chamada API (login `/api/*` e rotas `/backend/*`); o host do preview serve apenas a SPA no navegador. Comandos devem ser de uma linha só (quebra de linha ao colar trunca a URL e gera 404 falso — AP-2026-09-22-0915).
- Quando aplicar: qualquer roteiro humano ou prova automatizada contra o ambiente de teste Skip.
- Quando não aplicar: navegação normal no navegador (aí o host do preview é o correto).
- Confiança: alta — comportamento reproduzido nos dois hosts na mesma sessão.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
