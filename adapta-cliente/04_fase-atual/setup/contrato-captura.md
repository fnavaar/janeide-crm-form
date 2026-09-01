# Contrato de Setup — Captura de Lead e Origem (F1-T01)

**Task:** F1-T01 — Fechar contrato de captura, origem, webhook, CRM e dedupe
**SPEC:** SPEC-1-001
**Dono:** Matheus Silva
**Criado em:** 2026-08-18 por Janeidinha
**Estado:** CONFIRMADO (2026-08-31) — itens 1 a 7 confirmados; item 8 parcialmente confirmado (desenho do agente confirmado; citação de exigência regulatória pendente de fonte oficial)

> Este documento registra as 7 decisões que precisam ser fechadas para destravar a leva 2 da
> Fase 1. Cada item tem dono, estado e o que precisa para fechar. Nenhum item pode ser presumido
> ou inventado — ausência de decisão vira bloqueio registrado.

## Itens de decisão

### 1. Fonte de WhatsApp

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** usar um **segundo número, dedicado à captura automatizada de leads pelo
  site**, deixando o número atual (WhatsApp Business app, 6 anos de histórico) **intocado** — o
  atendimento atual continua como está, sem risco de migração.
- **Integração do segundo número:** **Cloud API da Meta direta** (sem BSP), conforme decisão de
  Matheus/Janeide — mais barato, sem camada extra; nós mantemos webhooks/tokens.

### 2. CRM fonte / destino do lead

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO para a Fase 1** (2026-08-31)
- **Decisão fechada:** na Fase 1 o destino do lead é o **próprio painel (Skip Cloud)** — não há
  integração automática com a Kenlo e não haverá neste momento. A operação segue com a Kenlo em
  paralelo, **sem migração**.
- **Impacto:** a fonte de verdade de leads nesta etapa é o **painel próprio**, sem dependência
  de homologação externa. Decisões sobre substituição futura da Kenlo (sistema interno completo)
  ficam para fase posterior, fora do escopo deste checklist.

### 3. Mecanismo de captura (webhook/API)

- **Dono:** Matheus Silva
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** **webhook nativo do WhatsApp Cloud API**, com **endpoint hospedado no
  próprio Skip Cloud**. Quando o lead clica no link do site e inicia a conversa, a Meta envia o
  evento de mensagem de entrada via POST para o endpoint; o sistema processa e cria o evento de
  captura (idempotente por `capture_event_id`).
- **Validação de assinatura (obrigatória):** o endpoint **valida a assinatura do webhook** para
  garantir que a chamada veio da Meta e impedir eventos falsos de captura:
  - **GET (verificação inicial):** conferir `hub.verify_token` e responder `hub.challenge`;
  - **POST (eventos):** verificar o header **`X-Hub-Signature-256`** — recalcular HMAC-SHA256 do
    corpo bruto usando o **App Secret** da Meta e comparar em tempo constante; se não bater,
    **rejeitar (401) e não processar**.
  - Fonte oficial: [Create a webhook endpoint — Meta for Developers](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/create-webhook-endpoint)
- **Impacto:** nenhum evento falso consegue virar captura sem o App Secret; endpoint seguro
  hospedado no Skip Cloud (sem infra extra).

### 4. Mapa de campos

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31), com 2 correções aplicadas
- **Campos da SPEC:** `capture_event_id`, `source_channel`, `campaign_ref`, `property_code`,
  `contact_ref`, `conversation_ref`, `occurred_at`, `consent_status`
- **Decisão fechada — distribuição dos 8 campos do evento × cartão Lead:**
  - `capture_event_id` → **só no evento** (referência, sem subir ao cartão);
  - `source_channel` → **cartão** (campo `origin`);
  - `campaign_ref` → **só no evento** — **não faz parte dos 15 campos** do modelo Lead do
    contrato-painel; **não adicionar como campo novo** no cartão;
  - `property_code` → **cartão**, opcional (preenchido quando o lead vem de imóvel específico;
    ausente → perfil de busca);
  - `contact_ref` → **só no evento** (referência da API); o cartão recebe **nome e telefone
    diretos** vindos do payload da conversa (`profile.name` + número);
  - `conversation_ref` → **cartão** (referência da conversa);
  - `occurred_at` → **dois campos diferentes no cartão**:
    - **data do primeiro contato** — gravada na **criação do cartão** (primeira captura do lead);
    - **data do último contato** — atualizada em **toda captura seguinte** do mesmo lead
      (equivalente ao `last_event_at` da SPEC);
  - `consent_status` → **cartão** (consentimento).
- **Para fechar:** revisar formatos/tamanhos destes campos contra o modelo de dados do painel na
  implementação (F1-T05/F1-T06); nenhum campo novo fora desta lista no cartão.

### 5. Permissões de escrita/leitura

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada — escopo de permissões:**
  - **Sistema (webhook/backend):** cria/atualiza lead e cartão com os dados do evento (nome,
    telefone, origem, perfil de busca, consentimento, datas). **Não** apaga histórico.
  - **SDR:** lê e trata pendências/próximo passo (matriz do contrato-painel — vê telefone de
    todos os leads).
  - **Corretor:** lê o cartão do próprio lead (telefone só do próprio).
  - **Admin/gestor:** lê tudo, revisa auditoria, corrige com motivo e auditoria.
  - **Nenhum papel** apaga histórico; alterações de origem exigem Admin com motivo.
- **Regra de conflito ambíguo no dedupe (adicionada):** quando o dedupe encontrar **conflito
  ambíguo** (ex.: telefone bate com um lead existente **mas** e-mail é diferente), o sistema
  **não** mescla nem decide sozinho — deve marcar o caso como **pendência para o SDR resolver
  manualmente**, preservando ambos os registros até a resolução humana.

### 6. Dedupe e papel do `capture_event_id`

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-27)
- **Decisão fechada:** dedupe por **telefone ou e-mail** na entrada; `lead_id` (UUID do primeiro
  contato) é a chave única do lead; `capture_event_id` fica como **referência do evento**,
  vinculado ao `lead_id`, e **não** é a fonte da chave. Cada nova captura da mesma pessoa
  reaproveita o `lead_id` existente.
- **Impacto:** idempotência da captura preservada sem quebrar o dedupe; `capture_event_id`
  registrado no evento e no vínculo lead–evento.

### 7. Ambiente de teste

- **Dono:** Matheus Silva / Adapta
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** o ambiente de teste do contrato-captura é o **mesmo projeto Skip
  dedicado** definido no contrato-painel (item 6) — um **único ambiente para todos os fixtures**
  (`cap-001`, `lead-001`, `imovel-001`, `visita-001`), já que os testes de fluxo completo (Fase
  Exercitar/Demonstrar) precisam que captura, painel, catálogo e pedido de visita rodem juntos.
- **Impacto:** fixture `cap-001` executado no projeto Skip de testes, com dados fictícios, sem
  PII real e sem misturar com produção.

### 8. Propósito específico do agente de IA (WhatsApp)

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** PARCIALMENTE CONFIRMADO (2026-08-31)
- **Desenho do agente (CONFIRMADO como boa prática):** agente de **qualificação de lead
  imobiliário com escopo claro** — identifica imóvel/perfil de busca, coleta contato, apresenta
  ficha, transfere ao SDR (**handoff humano**); **não** é assistente conversacional livre. Este
  desenho atende também a exigência da política de automação da Meta (resposta automática deve
  ter caminho de escalada humano disponível — fonte oficial: [WhatsApp Business Messaging
  Policy](https://business.whatsapp.com/policy)).
- **Citação de exigência regulatória (PENDENTE DE CONFIRMAÇÃO):** o usuário relatou que "desde
  janeiro/2026 a Meta exige que qualquer agente automatizado no WhatsApp tenha propósito
  específico e definido". **Não encontramos fonte oficial confirmável** com essa redação exata e
  a data. Existem documentos oficiais sobre banimento de **chatbots de IA de propósito geral**
  (a partir de 2026) e **política de automação com escalation humano**, mas a citação exata
  "jan/2026 · propósito específico" **permanece PENDENTE** — **não deve ser tratada como fato
  fechado** até fonte oficial ser citada.
- **Para fechar:** obter/citar a fonte oficial da Meta com a redação exata da exigência, se
  existir; caso contrário, manter como boa prática desenhada, não como requisito regulatório
  verificado.

## Pendência para produção (não passar despercebida)

- **Troca obrigatória do `META_APP_SECRET` real antes de publicação em produção**
  - O valor configurado hoje no projeto de teste `janeide-teste-fase-1-ba587` é um **secret de
    TESTE fictício** (usado só para validar o fluxo).
  - **Ação antes de publicar em produção:** Matheus Silva troca o `META_APP_SECRET` pelo
    **App Secret real do app da Meta (Cloud API)** no painel de secrets do Skip Cloud. Sem isso,
    o webhook em produção rejeitará todos os eventos (assinatura inválida) ou aceitará apenas os
    que baterem com o valor errado.
  - Referência: changelog 2026-09-01 · STATUS "Pendências de produção".

## Fixture de teste

O fixture `cap-001` foi criado em `04_fase-atual/fixtures/cap-001.json` com valores fictícios
conforme os campos da SPEC-1-001. Não contém PII real. Deve ser validado contra o ambiente
aprovado quando os itens acima forem fechados.

## Próximo passo

Realizar a **call de setup** com Matheus Silva (e Janeide Xavier quando aplicável) para fechar
os 7 itens. Cada decisão fechada deve ser registrada neste documento e no `changelog.md`.
Itens não resolvidos permanecem como bloqueio registrado em `STATUS.md`.