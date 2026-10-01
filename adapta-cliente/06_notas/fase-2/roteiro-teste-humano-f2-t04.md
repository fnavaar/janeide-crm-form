# F2-T04 — Roteiro de teste humano (Janeide)

**Ambiente:** preview `https://janeide-teste-fase-1-ba587--preview.goskip.app` (não publicado)
**Build:** 0.0.91 (`085a804`) — QA 5/5 PASS
**Objetivo:** provar CA-2-010, CA-2-011 e CA-2-012 com seus próprios olhos.
**Como usar:** copie e cole os comandos no Terminal (macOS) ou Prompt/PowerShell; o resultado esperado está em cada passo. Ao lado de cada passo, marque ✓ ou ✗. Nada aqui expõe senha ou dado pessoal — as credenciais de teste ficam só no cofre do Skip.

**Contas de teste (você define/guarda as senhas no cofre Skip; os secrets já existem):**
- Admin: conta do secret `AUDIT_F2_T02_CREDENTIALS`
- SDR: `F2_T02_SDR_CREDENTIALS`
- Corretor: `F2_T02_CORRETOR_CREDENTIALS`
- Outro (sem permissão): `F2_T04_OUTRO_CREDENTIALS`

---

## Parte A — Estados distintos do catálogo (CA-2-010)

> Prova que "Consulte", ausente, vencido, inativo e divergente aparecem como estados diferentes, sem inventar dado.

**A1 — Item válido com preços zerados (não é "Consulte"):**
```
curl -s "https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev/backend/v1/catalogo/buscar?code=F2-T01-001" -H "Authorization: TOKEN_SDR"
```
Esperado: 200; `price: null` (campo presente, sem valor) — NÃO "Consulte" e NÃO 0. Isso confirma a decisão B2-01 (zero monetário do `.xls` = não preenchido). `valid_until: 2026-10-15`, `catalog_version: cat-20260915-fac83f9cf10a`.

**A2 — Item vencido não aparece como opção ativa:**
```
curl -s "https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev/backend/v1/catalogo/buscar?code=F2-T01-004" -H "Authorization: TOKEN_SDR"
```
Esperado: vazio/`empty_state` com motivo de vigência — nunca oferecido como ativo.

**A3 — PENDÊNCIA REGISTRADA (decisão de Janeide, 01/10/2026 — não recebe ✓/✗):**
A UI da busca mostra "Consulte" tanto para preço **ausente** (`price: null`) quanto para preço **sob consulta**. O SDR, ao ver "Consulte" na tela hoje, **não consegue saber** se é "preço sob consulta" (precisa perguntar para alguém) ou "preço nunca cadastrado" (possível erro de dado faltando). Isso pode confundir o atendimento ao cliente. Dívida aceita conscientemente nesta task; a correção em task futura é **PRIORIDADE** — não é só um detalhe técnico de exibição.

✓/✗ A1 ___  A2 ___  A3: PENDÊNCIA registrada (não aplica)

---

## Parte B — URL insegura e item inválido (CA-2-011)

**B1 — Item com mídia insegura não é oferecido como ativo:**
```
curl -s "https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev/backend/v1/catalogo/buscar?code=F2-T01-005" -H "Authorization: TOKEN_SDR"
```
Esperado: `total: 0` com `empty_state` — o item F2-T01-005 está `pending` (mídia insegura bloqueada na carga) e não pode aparecer como opção ativa (CA-2-011). A URL `http://untrusted.invalid/...` não deve aparecer em nenhuma resposta.

**B2 — Código inexistente não inventa imóvel:**
```
curl -s "https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev/backend/v1/catalogo/buscar?code=NAO-EXISTE-999" -H "Authorization: TOKEN_SDR"
```
Esperado: `empty_state` (vazio honesto), sem sugestão aproximada.

✓/✗ B1 ___  B2 ___

---

## Parte C — Permissão por papel (CA-2-012)

> Repita os 4 comandos trocando apenas o papel. `TOKEN_X` = token de login do papel X (obtido em `/api/collections/users/auth-with-password` com identity/senha do cofre).
>
> **ID real do lead:** o roteiro NÃO traz um lead fixo. Rode primeiro o comando de **listagem**; no JSON da resposta, cada item tem o campo **`lead_id`** (ex.: `LEAD-...`). Copie esse valor e use na URL do cartão. Não use o campo `id` de 15 caracteres — o cartão busca pelo `lead_id`. Se a listagem vier vazia, pare e me avise.

**C1 — `outro` NÃO lê lead (403 em tudo):**
```
curl -s -o /dev/null -w '%{http_code}\n' "https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev/api/collections/leads/records?perPage=1" -H "Authorization: TOKEN_OUTRO"
curl -s -o /dev/null -w '%{http_code}\n' "https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev/backend/v1/painel/lead/LEAD_ID_REAL" -H "Authorization: TOKEN_OUTRO"
```
Esperado: **403** nos dois. (404 no cartão = `lead_id` inexistente — confira se copiou da listagem.)

**C2 — Papéis autorizados leem (200):** mesmos comandos com `TOKEN_SDR`, `TOKEN_CORRETOR`, `TOKEN_ADMIN` e o `LEAD_ID_REAL`.
Esperado: **200** nos três. (Corretor vê telefone só do lead atribuído a ele — regra F1-T10 preservada; conferir no cartão que `phone_visible` reflete isso.)

**C3 — Sem token = 401 (já provado pela assistente nos logs):** list/view/cartão sem `Authorization` retornaram 401 no host interno em 0.0.91.

✓/✗ C1 ___  C2 ___  C3 (informativo) ___

---

## Resultado

- Total de passos: 7 obrigatórios (A1–A2, B1–B2, C1–C2) + A3 como pendência registrada + C3 informativo.
- Se tudo der o esperado: responda "testei e funcionou" que eu fecho a task.
- Se algo falhar: me diga qual passo e o que apareceu — abro debug na hora, sem concluir nada.


## Ajuste do roteiro — 2026-10-01 17:40

- A1: Janeide observou `price: null` onde o roteiro esperava `0`. Verificado no código do hook de importação: a linha F2-T01-001 é gravada com `price/condominium_fee/iptu: null` por decisão B2-01 ("zero monetário = não preenchido"). `null` é o comportamento correto; o roteiro foi corrigido (esperado agora: `price: null`, não "Consulte", não 0). Nenhuma alteração de código foi necessária.


## Correção C2 — 2026-10-01 18:05

- C2 do SDR com `LEAD-TESTE-001` retornou 404: o ID era placeholder do roteiro, não lead real. 404 = "lead not found" (o hook busca por `lead_id`); permissão negada seria 403 e ausência de token, 401. Listagem do SDR (200) confirma que a rota e a permissão estão corretas.
- Roteiro corrigido: o cartão agora usa `LEAD_ID_REAL` copiado do campo `lead_id` da listagem (não o `id` de 15 caracteres). Instruções e diferença 403/404/401 anotadas no roteiro.
