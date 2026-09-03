# AP-2026-09-03-1145-goja-funcoes-fora-do-callback

- Status: candidato
- Escopo: projeto do cliente (Skip Cloud, hooks JS)
- Task/SPEC: F1-T07 / SPEC-1-003
- Sinal: ao definir `function safeArray(v) {...}` **fora** do `routerAdd(...)` (rodapé do arquivo), o callback lançou `ReferenceError: safeArray is not defined at /pb.js:53` em runtime (status 0 / 500 com corpo vazio). O guia oficial dos hooks Skip documenta: *"Top-level function declarations and const/let/var are NOT accessible inside routerAdd, onRecord* or cronAdd callbacks at runtime"* — o runtime é goja, cada callback roda em VM separada; só o que está **dentro** do callback (ou globais `$app`, `$security`, `routerAdd`, etc.) é visível. O build/QA estático não pega isso (a função existe no arquivo), só o teste em runtime.
- Regra reutilizável: em hooks da Skip (routerAdd/onRecord*/cronAdd), manter **toda função auxiliar declarada DENTRO do callback** (ou inline). Nunca depender de helper no escopo do arquivo. Validar sempre com uma chamada real em runtime (com auth) além do QA.
- Quando aplicar: toda escrita de hook na Skip Cloud.
- Quando não aplicar: não se aplica a migrations (que rodam em escopo próprio) nem a código fora de hooks.
- Confiança: alta — erro real reproduzido 2x nos logs e corrigido com inline (deploy 0.0.29).
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.