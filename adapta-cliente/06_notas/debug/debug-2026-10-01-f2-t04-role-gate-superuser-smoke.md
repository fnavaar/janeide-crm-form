# Debug Summary — F2-T04 role gate e smoke do superuser

**Data:** 2026-10-01
**Task/SPEC:** F2-T04 / SPEC-2-002, CA-2-012
**Ambiente:** Skip 55154, preview não publicado.

## Sintoma e reprodução

- A pipeline Skip 0.0.87 (`2ac9b2a`) completou setup, análise estática, build, integrações e testes (5/5). A migration `0032_f2_t04_leads_role_gate` ficou aplicada; leitura de volta confirmou `listRule`/`viewRule` de `leads` permitindo somente `admin`, `sdr` e `corretor`.
- A pipeline 0.0.88 (`cadd8ea`) passou setup/static/build/test mas falhou em integrations. Erro literal: `Hook leads_read_role_gate: Deploy of 'leads_read_role_gate' was reverted: with it loaded the platform's own superuser was refused (rejected, status 401: Auth required.), which locks the platform out of the app: no later deploy, migration or read could reach it. A routerUse/onBootstrap/onServe hook that throws breaks every route of the app; an onRecordAuth*Request hook that returns without e.next() breaks every login; an auth hook registered without a collection (e.g. onRecordAuthRequest(handler) instead of onRecordAuthRequest(handler, 'users')) also runs for the platform's superuser login, and refusing it locks the platform out of the app; a routerUse gate must never block /api/collections/_superusers/* or /_/, and must let superuser requests (e.hasSuperuserAuth()) through; any hook that crashes the boot takes the whole instance down. The previous hook set was restored and the instance is healthy again. Fix the hook and deploy again.`

## Diagnóstico / limite

- A cadeia causal observável é: o hook global `routerUse` não passou no smoke da sessão superuser; o pipeline detectou o bloqueio e declarou que restaurou o hook set anterior.
- O código no working tree tinha um `401` condicional a `!e.auth` e um bypass `hasSuperuserAuth()`; movi a checagem de sessão para depois da correspondência específica da rota de coleção `leads`. Esse ajuste foi gravado no working tree depois da falha, mas não foi validado por novo build.
- Causa final do smoke ainda não confirmada, porque a chamada seguinte de patch realtime e todas as leituras do Skip foram recusadas pelo MCP (`Forbidden`). Não declarar o runtime/revisão atual como saudável além do que o resultado QA afirmou.

## Estado e risco recuperável

- Migração 0032 está aplicada e a regra RLS foi lida de volta; a middleware foi revertida pelo pipeline de 0.0.88 conforme a mensagem de erro.
- Nenhuma prova autenticada de `role=outro`, `sdr`, `corretor` ou `admin` foi executada; não afirmar 403 ou leitura aprovada.
- Um hook temporário `test_f2_t04_role_matrix.js` e o secret temporário `F2_T04_ROLE_MATRIX_PROBE_KEY` foram criados para a matriz sem devolver token, credencial ou PII. MCP Skip tornou-se indisponível antes de confirmar se o hook/secret foram removidos; tratar limpeza como pendente e não chamar a rota temporária.
- Projeto não foi publicado. A única próxima ação é recuperar acesso ao MCP Skip, conferir versão/working tree/secret, remover sonda e chave, corrigir a exceção do superuser e então testar em QA antes de executar matriz de papéis.

## Resolução — 2026-10-01

- Janeide removeu manualmente a sonda (hook esvaziado) e o secret `F2_T04_ROLE_MATRIX_PROBE_KEY` pelo painel Skip; remoção confirmada por leitura de volta. Acesso MCP restaurado.
- Bypass de superuser aplicado também no realtime; 0.0.91 (`085a804`) QA 5/5 PASS, incluindo o smoke do superuser.
- Prova anônima no host interno: list/view de `leads` e cartão = 401 (o 200 no host do preview é fallback SPA `text/html`).
- Matriz autenticada validada por teste humano aprovado por Janeide: `outro` = 403 em listagem e cartão; SDR/Corretor/Admin = 200; regra F1-T10 do telefone preservada.
