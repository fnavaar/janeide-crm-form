# Controle de aprendizado contínuo

- 2026-08-18T10:58-03:00 · task F1-T01 · capturado · `AP-2026-08-18-1058-leva1-contrato.md` — tasks da leva 1 são fechamento de contrato, não código; critério aceita bloqueio registrado.
- 2026-08-26T14:14-03:00 · task F1-T02 · capturado · `AP-2026-08-18-1058-leva1-contrato.md` — mesmo padrão da F1-T01 confirmado por segunda instância.
- 2026-08-26T16:11-03:00 · task F1-T03 · capturado · `AP-2026-08-18-1058-leva1-contrato.md` — padrão de contrato de setup confirmado por terceira instância.
- 2026-08-26T16:25-03:00 · task F1-T03 · sem sinal reutilizável · correção pontual de nomenclatura (Quelo=Kenlo).
- 2026-08-26T16:50-03:00 · task F1-T04 · capturado · `AP-2026-08-18-1058-leva1-contrato.md` — padrão de contrato de setup confirmado por quarta instância.
- 2026-09-01T16:05-03:00 · task F1-T05 · capturado · `AP-2026-09-01-1605-skip-record-load.md` — criar record é `new Record(col)` + `load(data)`; `new Record('nome', data)` causa 500.
- 2026-09-03T11:35-03:00 · task F1-T06 · capturado · `AP-2026-09-03-1135-secret-no-chat.md` — credencial de teste não deve aparecer no chat; usuário define no secret, agente recria sem ver valor.
- 2026-09-03T12:24-03:00 · task F1-T07 · capturado · `AP-2026-09-03-1140-github-pos-push-validacao.md` — validar conteúdo publicado no GitHub (ler de volta) após push via MCP; evitar typos de transcrição.
- 2026-09-03T12:58-03:00 · task F1-T07 · capturado · `AP-2026-09-03-1145-goja-funcoes-fora-do-callback.md` — hooks da Skip: funções auxiliares devem ficar DENTRO do callback (goja); validar runtime além do QA.
- 2026-09-03T13:25-03:00 · task F1-T08 · capturado · `AP-2026-09-03-1150-actor-id-em-vez-de-email.md` — hooks Skip: created_by/cancelled_by com actor.id (email pode ser vazio); erro genérico no frontend exige consulta aos logs.
- 2026-09-03T14:04-03:00 · task F1-T08 · capturado · `AP-2026-09-03-1155-datetime-local-deve-virar-rfc3339.md` — datas de datetime-local devem ser convertidas para RFC3339 com offset antes do PocketBase; erro de save aparece nos logs.
- 2026-09-03T14:36-03:00 · task F1-T08 · capturado · `AP-2026-09-03-1200-dedupe-deve-ignorar-registros-cancelados.md` — dedupe deve filtrar estados ativos (nunca findFirstRecordByData por chave parcial com estados).
- 2026-09-04T12:53-03:00 · task F1-T09 · capturado · `AP-2026-09-04-1200-hmac-gerado-com-python.md` — assinatura HMAC gerada com Python (openssl do Mac/LibreSSL falhava); secret de teste rotaciona depois.
- 2026-09-07T17:27-03:00 · task F1-T10 · capturado · `AP-2026-09-07-1727-writes-skip-validar-com-listagem-e-write-back.md` — validar write com leitura de volta/listagem; migration idempotente pode aplicar sem efeito (secret ausente, lookup por chave canônica que não existe); diagnosticar "não apareceu" checando bundle → endpoint → cache.
- 2026-09-07T18:15-03:00 · task F1-T11 · capturado · `AP-2026-09-07-1815-campo-json-em-goja-nao-e-array-js.md` — campo JSON em goja pode voltar como array de BYTES (prova: 84/142/78 = bytes exatos do JSON.stringify); normalizar com detecção de bytes + toList conservador; contagens absurdas idênticas entre deploys = formato do dado, não cache; provar lógica em Node antes de re-teste humano.
- 2026-09-07T19:07-03:00 · task F1-T11 · capturado · convenções PocketBase number e requestInfo: campo number vazio normaliza para 0; usar `price > 0` como informado na Fase 1; corpo JSON da rota via `e.requestInfo().body`; preço "consulte" requer revisão futura do modelo.
- 2026-09-08T23:45-03:00 · task F1-T12 · capturado · idempotência de cancelamento deve ser comprovada no endpoint autenticado; botão oculto na UI após cancelamento não substitui a prova de segunda chamada; verificar preservação de cancelled_at/cancel_reason e ausência de novo registro.
- 2026-09-09T00:15-03:00 · task F1-T13 · capturado · HMAC de demonstração com secret temporário conhecido permitiu provar criação nova e duplicidade sem expor segredo; rotação do secret deve ser gate antes de prosseguir.
