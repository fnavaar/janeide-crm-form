#!/usr/bin/env bash
# F1-T09 — Verificação dos 4 cenários de borda da captura (SPEC-1-001)
# Uso: META_APP_SECRET=<seu-secret-de-teste> bash f1-t09-verificacao.sh
# O secret vem de variável de ambiente — NUNCA digite no código/chat.
set -euo pipefail

B="${BASE_URL:-https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev}"
SECRET="${META_APP_SECRET:?Defina META_APP_SECRET no ambiente}"

# helper: assinatura HMAC-SHA256 (hex) do body
sign() {
  printf '%s' "$1" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}'
}

req() { # req <nome> <body> <esperado>
  local nome="$1" body="$2" esperado="$3" sig
  sig=$(sign "$body")
  echo "== $nome (espera $esperado) =="
  curl -s -o /tmp/f1t09_resp.json -w "HTTP %{http_code}\n" --max-time 15 \
    -X POST "$B/backend/v1/whatsapp/webhook" \
    -H "Content-Type: application/json" \
    -H "X-Hub-Signature-256: sha256=$sig" \
    -d "$body"
  cat /tmp/f1t09_resp.json; echo; echo
}

# 1) Inválido: source_channel proibido -> 400
req "1-invalido-source-channel" '{"capture_event_id":"borda-01","source_channel":"telegram","property_code":"CASAS-TURIM-001","consent_status":"opt_in"}' "400"

# 2) Inválido: property_code inexistente no catálogo -> 200 pending invalid_property_code (após correção)
req "2-invalido-property-code" '{"capture_event_id":"borda-02","source_channel":"instagram","property_code":"CASAS-FANTASMA-999","contact":{"name":"Lead Borda","phone":"+55-11-98888-7777"},"consent_status":"opt_in"}' "200 pending invalid_property_code"

# 3) Repetido: enviar 2x mesmo capture_event_id -> 201 created, depois 200 duplicate
echo "== 3-repetido (1ª vez: espera 201 created) =="
sig=$(sign '{"capture_event_id":"borda-03","source_channel":"instagram","property_code":"CASAS-TURIM-001","contact":{"name":"Lead Repetido","phone":"+55-11-97777-6666"},"consent_status":"opt_in"}')
curl -s -o /tmp/f1t09_a.json -w "HTTP %{http_code}\n" --max-time 15 -X POST "$B/backend/v1/whatsapp/webhook" -H "Content-Type: application/json" -H "X-Hub-Signature-256: sha256=$sig" -d '{"capture_event_id":"borda-03","source_channel":"instagram","property_code":"CASAS-TURIM-001","contact":{"name":"Lead Repetido","phone":"+55-11-97777-6666"},"consent_status":"opt_in"}'
cat /tmp/f1t09_a.json; echo
echo "== 3-repetido (2ª vez: espera 200 duplicate) =="
curl -s -o /tmp/f1t09_b.json -w "HTTP %{http_code}\n" --max-time 15 -X POST "$B/backend/v1/whatsapp/webhook" -H "Content-Type: application/json" -H "X-Hub-Signature-256: sha256=$sig" -d '{"capture_event_id":"borda-03","source_channel":"instagram","property_code":"CASAS-TURIM-001","contact":{"name":"Lead Repetido","phone":"+55-11-97777-6666"},"consent_status":"opt_in"}'
cat /tmp/f1t09_b.json; echo; echo

# 4) Opt-out: consent_status=opt_out -> 200 rejected (lead não criado)
req "4-optout" '{"capture_event_id":"borda-04","source_channel":"instagram","property_code":"CASAS-TURIM-001","contact":{"name":"Lead OptOut","phone":"+55-11-96666-5555"},"consent_status":"opt_out"}' "200 rejected"

# 5) Indisponibilidade (falha de save simulada): body que force erro -> por ora documentar
echo "== 5-indisponibilidade (falha de save) =="
echo "Simulação manual: falha de $app.save é difícil de forçar via curl (depende do ambiente)."
echo "Coberto por: try/catch no hook -> evento status=error + 503 save_failed (código em produção)."

echo
echo "Conferir nos logs/docs: captur_events com status pending(rejected/error) e lead único."
