# AP-2026-09-03-1155-datetime-local-deve-virar-rfc3339

- Status: candidato
- Escopo: projeto do cliente (Skip Cloud, frontend + PocketBase)
- Task/SPEC: F1-T08 / SPEC-1-004
- Sinal: no painel, ao preencher a janela estruturada (Início/Fim) e registrar, o pedido **não** era criado; apenas o texto livre funcionava. Causa: `<input type="datetime-local">` envia `2026-09-05T10:00` (sem timezone/segundos), e o PocketBase exige campo `date` em **RFC3339 com offset** (`2026-09-05T10:00:00-03:00`). O `rec.load` rejeitava (400) e o frontend mascara como "Falha ao registrar pedido". Texto livre passa porque não usa campo de data.
- Regra reutilizável: ao enviar datas de inputs `datetime-local` para o PocketBase, **converter para RFC3339 com timezone fixo** antes (ex.: `${v}:00-03:00` para America/Bahia). Nunca enviar o valor cru do input. E, em erro de save de data, o log do servidor mostra o campo exato (ex.: `requested_start: ...`) — consultar logs em vez de confiar na mensagem genérica.
- Quando aplicar: qualquer campo `date` no Skip/PocketBase alimentado por formulário (visitas, captura, prazos).
- Quando não aplicar: campos `text`/`json` (texto livre) ou datas já em RFC3339.
- Confiança: alta — reproduzido no teste (estruturado falha, texto livre funciona), corrigido no frontend (deploy 0.0.33, bundle com toRfc3339), QA verde.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.