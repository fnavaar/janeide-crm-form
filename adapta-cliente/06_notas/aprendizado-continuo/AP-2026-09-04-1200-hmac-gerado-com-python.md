# AP-2026-09-04-1200-hmac-gerado-com-python

- Status: candidato
- Escopo: projeto do cliente (verificação de webhook / assinatura)
- Task/SPEC: F1-T09 / SPEC-1-001
- Sinal: ao tentar rodar o script de verificação do webhook localmente, o `openssl dgst -sha256 -hmac` do **macOS (LibreSSL)** gerou assinatura que o servidor rejeitou (401) em 6 tentativas com secrets diferentes. O problema não era o secret — era a **formatação/ferramenta de assinatura local**. Solução: calcular o HMAC-SHA256 **com Python** (`hmac.new(secret, body, hashlib.sha256).hexdigest()`) e entregar os curls com a assinatura **pré-calculada**, eliminando a dependência do openssl local do usuário.
- Regra reutilizável: ao gerar assinaturas HMAC para webhooks, **não depender do `openssl` do ambiente do usuário** (LibreSSL vs OpenSSL pode divergir). Usar **Python `hmac`** (disponível e consistente) ou um valor de secret de teste que o agente conheça, calcular a assinatura do lado do agente e entregar o curl pronto. Para testes, definir um secret de teste próprio (com autorização) e rotacionar depois.
- Quando aplicar: qualquer verificação de webhook com `X-Hub-Signature-256`; geração de assinaturas para o usuário colar.
- Quando não aplicar: quando o usuário tem OpenSSL confiável ou o agente tem acesso ao secret.
- Confiança: alta — 6 falhas com openssl do Mac, resolvido com Python + secret de teste (5 cenários passaram).
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.