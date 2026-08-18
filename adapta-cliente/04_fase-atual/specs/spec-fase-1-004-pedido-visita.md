# SPEC-1-004 — registro de pedido de visita sem agenda integrada

**Fase:** 1  
**Status:** bloqueada  
**Dono:** SDR/atendente, com validação de negócio de Janeide  
**Origem no escopo:** C3 inicial, RQ-004/RQ-008, D-102, D-103, AC-102/AC-103  
**Degrau da solução:** construção mínima — registrar uma solicitação pendente de agenda no painel, sem reservar horário ou alocar corretor nesta fase.

## Contexto e decisões fechadas

- **Estado atual:** o pedido de visita interrompe o atendimento para consulta paralela de
  disponibilidade (`03-Projeto/01-Escopo.md`, §§2–4; `03-Projeto/requisitos.md`, RQ-004).
- **Estado desejado:** o SDR registra no cartão o pedido, imóvel, lead, preferência de janela e
  próximo passo, com estado `Pendente de agenda`, preservando a continuidade da conversa.
- **Decisões já fechadas:** toda visita futura exigirá corretor responsável; nesta fase não há
  agenda integrada, confirmação, liberação, lembrete ou no-show; não reservar horário por inferência.
- **Bloqueios:** **BLOQUEIO** — confirmar modelo de visita, timezone, campos de janela e fonte futura
  de agenda; esta SPEC pode registrar pedido, mas não autoriza booking.

## Resultado observável

Em um lead com ficha enviada, o SDR registra um pedido de visita com `visit_request_id`, lead,
imóvel, preferência de data/janela, canal, consentimento e estado `Pendente de agenda`. O cartão
mostra o próximo passo e o sistema não atribui corretor nem bloqueia agenda. O SDR pode recuperar a
pendência para completar a agenda na Fase 3.

## Limites e dependências

- **Inclui:** botão/ação manual de pedido; entidade mínima; estado pendente; janela estruturada ou
  texto marcado para esclarecimento; vínculo lead–imóvel; próximo passo; log.
- **Fora de escopo:** disponibilidade em tempo real; escolha/alocação de corretor; chave; reserva;
  confirmação T-2h; liberação; mensagem automática; no-show.
- **Entradas e pré-condições:** `lead_id`, `property_code/property_id`, ficha ou interesse
  confirmado, preferência de data/janela, timezone quando informado, consentimento e ator SDR.
- **Saídas/artefatos:** `visit_request_id`; estado `Pendente de agenda`; pendência/next step;
  auditoria.
- **Dependências e responsáveis:** painel/Lead — SPEC-1-002; ficha — SPEC-1-003; política e
  campos de visita — Janeide/Matheus/corretores.
- **Atores e permissões mínimas:** SDR cria/edita pedido pendente; gestor lê e corrige com motivo;
  sistema não cria reserva; corretor não é notificado nesta fase.
- **Superfícies/arquivos/configurações afetadas:** cartão de lead, entidade de pedido, fila de
  pendências e auditoria. Plataforma/armazenamento são **BLOQUEIO**.
- **Risco e plano B:** janela incompleta ou pedido duplicado; marcar `Precisa esclarecer` e criar
  uma pendência, sem criar reserva.
- **Rollback ou reversão:** cancelar pedido pendente com motivo, sem apagar histórico; voltar ao
  registro manual se painel indisponível.

## Dados e integrações

| Origem/destino | Fonte de verdade | Campos/contrato | Autenticação/permissão | Timeout/retry/idempotência | Tratamento de erro |
|---|---|---|---|---|---|
| Cartão Lead → pedido | painel e evento do SDR | `visit_request_id`, `lead_id`, `property_id/code`, `requested_start`, `requested_end`, `requested_text`, `timezone`, `status=Pendente de agenda`, `next_step`, `created_by`, `created_at` | SDR/gestor autorizados; sem agenda externa | dedupe por `visit_request_id`; retry não cria outro pedido | pendência de entrada e log |
| Pedido → futura agenda | nenhuma integração nesta fase | não enviar booking; apenas estado pendente | proibido criar slot/corretor/chave | não aplicar retry externo | manter no painel para Fase 3 |

| Regra de negócio | Condição | Ação/resultado | Exceção | Fonte |
|---|---|---|---|---|
| RN-1 Sem reserva | pedido criado na Fase 1 | estado sempre `Pendente de agenda` | nenhuma ação pode bloquear slot | Fase 1 do definitivo |
| RN-2 Vínculo obrigatório | imóvel/lead conhecidos | relacionar pedido a ambos | se faltar um, estado `Precisa esclarecer` | RQ-004/RQ-008 |
| RN-3 Janela honesta | data/janela estruturada ou texto livre | salvar o tipo de entrada e timezone | ausência vira pendência | RQ-004 |
| RN-4 Histórico | edição/cancelamento | registrar ator, horário e motivo | não apagar registro | RQ-010 |
| RN-5 Texto e PII mínimos | preferência chega em texto livre | tratar como dado, limitar ao necessário e escapar apresentação | conteúdo indevido ou PII excedente vira pendência | RQ-010 |

## Fluxo e regras

1. SDR abre o cartão após envio/consulta da ficha.
2. Seleciona `Registrar pedido de visita`.
3. Informa data/janela estruturada ou registra a preferência em texto com `Precisa esclarecer`.
4. Sistema valida lead/imóvel e cria `visit_request_id` idempotente.
5. Sistema mostra `Pendente de agenda`, próximo passo e responsável SDR.
6. Fase 3 poderá consumir o pedido; nenhum corretor ou horário é atribuído agora.

| Cenário | Dado/condição | Resultado esperado | Caminho de erro/recuperação |
|---|---|---|---|
| Principal | lead/imóvel e janela válidos | pedido pendente criado e exibido no cartão | nenhum |
| Texto livre | preferência sem início/fim | pedido `Precisa esclarecer`, sem reserva | SDR retoma com cliente |
| Duplicado | mesma ação/reenvio | um `visit_request_id` e log de repetição | reconciliar se dados divergirem |
| Incompleto | lead ou imóvel ausente | não criar pedido completo | pendência para SDR |
| Falha | painel indisponível | nenhum booking; registro manual orientado | reentrada posterior com correlação |

## Instruções de execução para o Ethos

1. **Ler antes de alterar:** `03-Projeto/02-Escopo-Definitivo.md` Fase 1 e §5; `03-Projeto/requisitos.md` RQ-004/RQ-008/RQ-010; SPEC-1-002/003.
2. **Alterar somente:** ação de pedido, entidade mínima, estado pendente, próximo passo e auditoria.
3. **Não alterar:** agenda, corretor, chave, reserva, confirmação, lembrete, no-show ou notificação externa.
4. **Executar nesta ordem:** validar vínculo → registrar pedido → testar janela → testar repetição → testar incompleto/falha → demonstrar.
5. **Parar e pedir validação quando:** campos, timezone, retenção, permissão ou qualquer integração de agenda for necessária.
6. **Estado válido ao parar:** pedidos pendentes não prometem horário; histórico e próximo passo permanecem visíveis.

## Checklist de execução

- [ ] modelo de pedido e estados aprovados;
- [ ] regra explícita de não reserva testada;
- [ ] permissão SDR/gestor e auditoria testadas;
- [ ] janela estruturada, texto livre, duplicidade e falha exercitados;
- [ ] pedido aparece no cartão e na fila de pendências;
- [ ] handoff para a Fase 3 documentado.

## Critérios de aceite

- [ ] **CA-1-13:** SDR cria um pedido relacionado a lead e imóvel com estado `Pendente de agenda`.
- [ ] **CA-1-14:** nenhum pedido da Fase 1 cria slot, corretor, chave ou reserva.
- [ ] **CA-1-15:** janela incompleta vira `Precisa esclarecer` e não é tratada como agendada.
- [ ] **CA-1-16:** repetição não duplica pedido e alteração/cancelamento deixa motivo e histórico.

## TDD da SPEC

| Etapa | Prova | Comando/ação | Resultado esperado | Evidência |
|---|---|---|---|---|
| RED | processo atual | pedir visita e procurar registro único no painel | pedido fica em conversa/controle paralelo, sem estado recuperável | captura do estado atual |
| GREEN | lead/ficha de teste | registrar pedido com `lead-001`, `property-001`, janela e timezone | pedido pendente aparece no cartão com ID e próximo passo | captura + ID |
| GREEN | proteção de escopo | tentar confirmar horário/corretor pela Fase 1 | ação inexistente ou bloqueada; nenhuma reserva criada | log de bloqueio |
| REFACTOR/REGRESSÃO | texto livre, duplicidade e painel indisponível | executar três cenários | esclarecer/ignorar repetição/registrar pendência corretamente | relatório de cenários |

**Dados/fixtures:** `lead-001`, `property-001`, janela de teste e usuário SDR; plataforma e armazenamento
concretos são **BLOQUEIO**.
**Caminhos de erro obrigatórios:** lead/imóvel ausente, janela incompleta, repetição, permissão negada,
  painel indisponível, tentativa de booking e texto/PII não permitido.
**Evidência exigida:** cartão, pedido, estado, log, bloqueio de reserva e aceite do SDR/gestor.

## Handoff e operação

- **Como demonstrar:** abrir lead, registrar preferência e mostrar que o pedido está pendente sem reserva.
- **Como operar depois:** SDR retoma pendências; Fase 3 consome pedidos após fonte de agenda aprovada.
- **Como monitorar:** pedidos sem próximo passo, janela incompleta, duplicidades e idade da pendência.
- **Pendência conhecida:** modelo final, timezone e futura fonte de agenda.

## Tasks vinculadas

| ID | Task | Critério binário | Recorte da prova | Evidência | Status |
|---|---|---|---|---|---|
| F1-T04 | Fechar modelo do pedido de visita e regra de não reserva | estados, janela, timezone e dono do próximo passo aprovados | Contexto; Dados; Regras RN-1–RN-5 | decisão operacional e exemplo sem booking | PENDENTE |
| F1-T08 | Configurar registro de pedido pendente sem agenda | pedido vinculado recebe `Pendente de agenda` e próximo passo | Resultado; Fluxo 1–5; CA-1-13/14 | ID do pedido e cartão | BLOQUEADA |
| F1-T12 | Exercitar janela incompleta, duplicidade e tentativa de booking | pedido incompleto esclarece; repetição não duplica; booking é bloqueado | Cenários; RN-1–RN-5 | pedido, log e bloqueio de reserva | BLOQUEADA |
| F1-T16 | Demonstrar pedido pendente e handoff para Fase 3 | CA-1-13 a CA-1-16 passam sem reserva | TDD; Handoff | pedido, estado, bloqueio e aceite | BLOQUEADA |

## Emendas

<!-- Append-only: mudanças aprovadas depois da geração. -->

| Data | Origem do sinal | Micro-spec/task | Motivo |
|---|---|---|---|
| | | | |
