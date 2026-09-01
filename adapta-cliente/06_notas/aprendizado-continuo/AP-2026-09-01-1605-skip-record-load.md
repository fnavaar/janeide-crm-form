# AP-2026-09-01-1605 — Skip Cloud: criar records via `new Record(col)` + `load()`

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T05 / SPEC-1-001
- Sinal: ao implementar o webhook de captura no Skip Cloud (PocketBase goja), `new Record('collection_name', data)` + `$app.save` lançava **500 silencioso** (sem log). O padrão que funciona é `new Record(col)` (com `col = $app.findCollectionByNameOrId(...)`) + `record.load(data)` + `$app.save(record)`.
- Evidência: hooks diag2 (500 com construtor 2 args) vs diag3 (200 com `new Record(col)`+`load`); webhook final funcionando (`200 duplicate`). Raw body lido com `toString(e.request.body)` (docs PocketBase).
- Regra reutilizável: em hooks/migrations do Skip Cloud, **nunca** `new Record('nome', data)`; use `new Record(collection)` + `load(data)`. Rotas custom só em `/backend/v1/`; validação de assinatura com `$security.hs256(rawBody, secret)` (hex) sobre `toString(e.request.body)`.
- Quando aplicar: qualquer hook/migration futura no projeto Skip de teste/produção (F1-T06+).
- Quando não aplicar: fora do runtime Skip Cloud (Node/outros backends usam outros padrões).
- Confiança: alta — verificado empiricamente com diags e teste humano.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.