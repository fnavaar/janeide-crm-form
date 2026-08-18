# SPEC-1-001 — captura de lead e origem por link direto

**Fase:** 1  
**Status:** bloqueada  
**Dono:** Matheus Silva / equipe técnica, com validação operacional do SDR  
**Origem no escopo:** C1, RQ-001, D-101, D-102, AC-101/AC-102  
**Degrau da solução:** construção mínima — contrato de evento e adaptador isolado preservam a opção de manter Kenlo/Quelo ou trocar a fonte depois do inventário.

## Contexto e decisões fechadas

- **Estado atual:** o lead chega por Instagram, site, indicação ou WhatsApp e a captura/origem é
  tratada manualmente; o nome real da fonte CRM/WhatsApp e suas permissões ainda precisam ser
  reconciliados (`03-Projeto/requisitos.md`, RQ-001; `03-Projeto/02-Escopo-Definitivo.md`, §3–§4).
- **Estado desejado:** um link aprovado inicia a conversa e produz um evento rastreável que cria
  ou atualiza um lead único com origem e imóvel de interesse, ou cria pendência para o SDR.
- **Decisões já fechadas:** não substituir o CRM nesta fase; não disparar mensagem fora de template;
  preservar atendimento humano; não duplicar lead; falha de integração vira pendência.
- **Bloqueios:** **BLOQUEIO** — confirmar número/plataforma de WhatsApp, webhook ou mecanismo de
  captura, CRM fonte, mapa de campos, permissão de escrita e chave de idempotência com Matheus/Janeide.

## Resultado observável

Um link de teste com canal, campanha e código de imóvel aprovados leva ao WhatsApp e gera, na
fonte de leads aprovada, um registro relacionável com origem, imóvel e conversa. Repetir o mesmo
evento não cria um segundo lead. Se o provedor ou CRM falhar, o SDR vê uma pendência com motivo e
referência de correlação.

## Limites e dependências

- **Inclui:** padrão de parâmetros do link; recepção do evento; validação mínima; upsert de lead;
  origem/código; deduplicação por evento; log de sucesso/erro; pendência do SDR.
- **Fora de escopo:** escolha final de fornecedor; migração/substituição de CRM; campanhas novas;
  qualificação IA; envio autônomo de conversa; agenda e no-show.
- **Entradas e pré-condições:** link aprovado; conversa iniciada; canal autorizado; `capture_event_id`,
  `source_channel`, `campaign_ref` quando houver, `property_code` quando houver, `contact_ref`,
  `conversation_ref`, `occurred_at` e `consent_status` disponíveis.
- **Saídas/artefatos:** lead criado/atualizado; evento de captura; log de correlação; pendência
  recuperável quando falhar.
- **Dependências e responsáveis:** WhatsApp e CRM — Matheus/Janeide; conteúdo e operação — SDR;
  link/campanha — marketing/Matheus.
- **Atores e permissões mínimas:** sistema pode criar/atualizar campos aprovados; SDR lê e trata
  pendências; gestor lê auditoria; nenhum papel apaga histórico.
- **Superfícies/arquivos/configurações afetadas:** link de origem; adaptador de captura; registro
  de Lead; fila de pendências; log de eventos. O repositório/plataforma concreta é **BLOQUEIO**.
- **Risco e plano B:** webhook ausente, código inválido, duplicidade ou CRM indisponível; manter
  evento bruto/correlação e criar fila manual do SDR, sem descartar a conversa.
- **Rollback ou reversão:** desativar links novos e voltar à entrada manual; não apagar leads ou
  eventos já registrados; reprocessar somente pelo identificador idempotente.

## Dados e integrações

| Origem/destino | Fonte de verdade | Campos/contrato | Autenticação/permissão | Timeout/retry/idempotência | Tratamento de erro |
|---|---|---|---|---|---|
| Link aprovado → canal de WhatsApp → adaptador | plataforma de WhatsApp a confirmar | `capture_event_id`, `source_channel`, `campaign_ref`, `property_code`, `contact_ref`, `conversation_ref`, `occurred_at`, `consent_status` | conta/número e webhook autorizados; acesso mínimo de leitura da conversa e criação de evento | timeout e retry conforme provedor a confirmar; sem retry cego; dedupe primário por `capture_event_id` | pendência com erro, timestamp e correlação |
| Adaptador → fonte de Lead | CRM Kenlo/Quelo ou fonte aprovada após D-101 | `lead_id`, `contact_ref`, `phone`, `origin`, `property_code`, `status=Em Atendimento`, `created_at`, `updated_at` | criação/atualização apenas nos campos autorizados; sem migração | upsert idempotente; chave alternativa ao `capture_event_id` é **BLOQUEIO** | manter evento pendente e não marcar sucesso |

| Regra de negócio | Condição | Ação/resultado | Exceção | Fonte |
|---|---|---|---|---|
| RN-1 Não duplicar | evento recebido | procurar `capture_event_id` antes do upsert | se não houver ID, parar e pedir decisão de deduplicação | RQ-001; D-101 |
| RN-2 Preservar origem | canal/campanha/código presentes | gravar valores originais, sem normalização destrutiva | valor inválido vira pendência | C1; RQ-001 |
| RN-3 Consentimento | contato iniciado e política aprovada | registrar estado de consentimento | ausência/opt-out impede ação de mensagem | RQ-010; escopo definitivo §6 |
| RN-4 Falha recuperável | provedor/CRM indisponível | guardar correlação e criar tarefa SDR | não criar lead parcial como concluído | RQ-001 |
| RN-5 Entrada externa e PII | parâmetro chega por link/webhook | aceitar somente canais/campos permitidos, escapar valores e minimizar/redigir PII em logs | valor não permitido é rejeitado e vira pendência | RQ-010 |

## Fluxo e regras

1. SDR/marketing publica somente link aprovado com `source_channel` e `property_code` válidos.
2. Lead clica e inicia conversa; o canal fornece o evento e a referência da conversa.
3. Adaptador trata os parâmetros como entrada não confiável, valida campos permitidos, consentimento e código; não inventa campo ausente nem executa valor recebido.
4. Sistema verifica `capture_event_id` e executa upsert na fonte autorizada.
5. Sistema relaciona origem e imóvel, registra `Em Atendimento` e envia confirmação interna ao painel.
6. Falha em qualquer dependência gera pendência com motivo, referência e próximo responsável.

| Cenário | Dado/condição | Resultado esperado | Caminho de erro/recuperação |
|---|---|---|---|
| Principal | evento novo, fonte/código válidos | um lead com origem, imóvel e correlação | nenhum |
| Repetido | mesmo `capture_event_id` | nenhum segundo lead; log de idempotência | se o destino divergir, pendência de reconciliação |
| Limite | código ausente ou inválido | lead pode ser criado sem imóvel somente se a fonte aprovar; caso contrário, pendência | SDR completa contexto sem apagar origem |
| Falha | CRM/WhatsApp indisponível | evento não é sucesso; pendência preserva referência | reprocessamento manual após autorização |
| Privacidade | opt-out ou permissão negada | não enviar e não atualizar campo não autorizado | registrar bloqueio e escalar ao responsável |

## Instruções de execução para o Ethos

1. **Ler antes de alterar:** `03-Projeto/02-Escopo-Definitivo.md` §§2–6 e Fase 1; `03-Projeto/requisitos.md` RQ-001/RQ-010; setup de conectores; decisão D-101.
2. **Alterar somente:** link/contrato de captura, adaptador mínimo, upsert autorizado, log e pendência.
3. **Não alterar:** CRM fonte, migração, regras de consentimento, templates, agenda, no-show ou classificação IA.
4. **Executar nesta ordem:** confirmar acesso → validar contrato → testar evento novo → testar repetição → testar falha → registrar evidências.
5. **Parar e pedir validação quando:** qualquer campo, endpoint, permissão, chave de dedupe ou fonte não estiver confirmado.
6. **Estado válido ao parar:** links antigos continuam utilizáveis; nenhum evento é perdido; pendências têm correlação.

## Checklist de execução

- [ ] fonte de WhatsApp, CRM, webhook e permissões confirmadas;
- [ ] contrato de campos e chave de idempotência aprovados;
- [ ] link de teste publicado somente no ambiente autorizado;
- [ ] caminho principal, repetição, código inválido, opt-out e indisponibilidade exercitados;
- [ ] logs e pendências anexados à evidência da SPEC, sem PII bruta fora dos campos autorizados;
- [ ] dono operacional e handoff para SDR confirmados.

## Critérios de aceite

- [ ] **CA-1-01:** link aprovado gera um único lead relacionável com origem e código de imóvel na fonte autorizada.
- [ ] **CA-1-02:** repetir o mesmo evento não cria duplicidade e deixa log de idempotência.
- [ ] **CA-1-03:** código inválido, permissão negada ou indisponibilidade gera pendência com motivo e correlação.
- [ ] **CA-1-04:** opt-out impede mensagem/atualização não autorizada e fica auditável.

## TDD da SPEC

| Etapa | Prova | Comando/ação | Resultado esperado | Evidência |
|---|---|---|---|---|
| RED | fluxo atual manual | executar link sem captura estruturada e consultar painel/fonte | não existe lead rastreável por origem/código; registrar estado atual | captura/log do estado atual |
| GREEN | evento novo válido | executar fixture `capture_event_id=cap-001`, `source_channel=instagram`, `property_code=CASAS-TURIM-001` no ambiente aprovado | um lead `Em Atendimento`, origem e código preservados | ID do lead, log e captura da tela |
| GREEN | repetição | reenviar `cap-001` | nenhum segundo lead; evento marcado repetido | log de idempotência |
| REFACTOR/REGRESSÃO | inválido, opt-out e indisponibilidade | executar os três cenários no ambiente aprovado | pendência/ bloqueio correto, sem sucesso falso ou envio indevido | relatório de cenários |

**Dados/fixtures:** fixture de captura acima; telefone e conversa de teste devem ser fornecidos
pela equipe sem usar dado real desnecessário. O ambiente, provedor e armazenamento são **BLOQUEIO**.
**Caminhos de erro obrigatórios:** campo ausente, código inválido, parâmetro não permitido,
  repetição, opt-out, permissão negada, timeout e CRM indisponível.
**Evidência exigida:** log/evento, registro do lead, captura do painel e aceite do SDR/Matheus.

## Handoff e operação

- **Como demonstrar:** publicar link de teste, iniciar conversa, localizar lead e repetir o evento.
- **Como operar depois:** marketing publica links; SDR trata pendências; Matheus monitora integração.
- **Como monitorar:** eventos sem destino, duplicidades, falhas de canal e idade da fila.
- **Pendência conhecida:** toda a definição concreta de provedor, fonte, permissões e dedupe listada como BLOQUEIO.

## Tasks vinculadas

| ID | Task | Critério binário | Recorte da prova | Evidência | Status |
|---|---|---|---|---|---|
| F1-T01 | Fechar contrato de captura, origem, webhook, CRM e dedupe | fonte, campos, permissão e `capture_event_id` aprovados ou bloqueio registrado | Contexto; Dados e integrações; Instruções 1–5 | decisão/registro de setup e fixture `cap-001` | PENDENTE |
| F1-T05 | Configurar link e captura idempotente de lead | evento válido cria/atualiza um lead com origem e código | Resultado; Fluxo 1–5; CA-1-01/02 | ID do lead, log e captura | BLOQUEADA |
| F1-T09 | Exercitar bordas da captura e fila de pendência | inválido, repetido, opt-out e indisponível geram resultado correto | Cenários; RN-1–RN-5; caminhos de erro | relatório de quatro cenários | BLOQUEADA |
| F1-T13 | Demonstrar captura ponta a ponta e handoff ao SDR | CA-1-01 a CA-1-04 passam no fixture aprovado | TDD RED/GREEN/REGRESSÃO; Handoff | vídeo/capturas, logs e aceite SDR/Matheus | BLOQUEADA |

## Emendas

<!-- Append-only: mudanças aprovadas depois da geração. -->

| Data | Origem do sinal | Micro-spec/task | Motivo |
|---|---|---|---|
| | | | |
