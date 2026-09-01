# Contrato de Setup — Pedido de Visita sem Reserva (F1-T04)

**Task:** F1-T04 — Fechar modelo do pedido de visita e regra de não reserva
**SPEC:** SPEC-1-004
**Dono:** Janeide Xavier
**Criado em:** 2026-08-26 por Janeidinha
**Estado:** CONFIRMADO — 6/6 itens fechados (modelo/estados, campos, janela, timezone America/Bahia, fonte futura de agenda, dono do próximo passo)

> Este documento registra as decisões do pedido de visita. Replica o padrão dos contratos de setup
> anteriores (F1-T01/F1-T02/F1-T03). Nesta fase o sistema **registra o pedido como "Pendente de
> agenda" e NÃO reserva horário, não aloca corretor, não usa chave nem agenda** — reserva e
> confirmação ficam para a Fase 3.

## Itens de decisão

### 1. Modelo de pedido e estados

- **Dono:** Janeide Xavier / Matheus Silva
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada — estados da Fase 1:**
  - `Pendente de agenda` — estado principal; todo pedido válido sem reserva criada;
  - `Precisa esclarecer` — janela incompleta ou vínculo lead/imóvel faltando (RN-2/RN-3); não é
    tratado como agendado (CA-1-15);
  - `Cancelado` — **adicionado por decisão de Janeide**: usado apenas quando o **lead ou o SDR
    cancela explicitamente** o pedido. Sem esse estado, um pedido cancelado continuaria
    aparecendo como `Pendente de agenda` e o SDR poderia tentar agendar algo que o lead desistiu.
- **Edição comum** (ex.: mudança de horário desejado) **não** muda de estado — só o cancelamento
  usa `Cancelado`. O histórico com motivo (RN-4) registra o porquê em ambos os casos.

### 2. Campos do pedido

- **Dono:** Janeide Xavier / Matheus Silva
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada — modelo do pedido (14 campos):**
  - os **11 campos da SPEC** como base: `visit_request_id`, `lead_id`, `property_code`,
    `requested_start`, `requested_end`, `requested_text`, `timezone`, `status`, `next_step`,
    `created_by`, `created_at`;
  - **nome do campo de imóvel:** `property_code` (não `property_id/code`) — alinhado ao mesmo
    campo já usado no catálogo e no modelo Lead; evita duas nomenclaturas para a mesma coisa;
  - **3 campos extras aprovados** para rastreabilidade do cancelamento (RN-4): `cancelled_by`,
    `cancelled_at`, `cancel_reason`.
- **Impacto:** `status` aceita os 3 estados; `requested_start`/`requested_end` quando o lead
  escolhe horário da agenda geral; `requested_text` quando não há horário compatível;
  `timezone` fixo America/Bahia; `cancelled_*` preenchidos apenas quando o status for `Cancelado`.

### 3. Janela estruturada vs. texto livre

- **Dono:** Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-26)
- **Decisão fechada:** o lead escolhe horário da **agenda geral** (janela estruturada); texto livre
  é usado **somente quando não há horário compatível**.
- **Impacto:** `requested_start`/`requested_end` preenchidos na maioria dos casos; `requested_text`
  reservado para o caso sem horário compatível, marcando `Precisa esclarecer` quando aplicável.

### 4. Timezone

- **Dono:** Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-26)
- **Decisão fechada:** timezone fixo **America/Bahia (-03:00)**.
- **Impacto:** todos os `requested_start`/`requested_end` e timestamps usam -03:00; sem variação
  por lead nesta fase.

### 5. Fonte futura de agenda

- **Dono:** Janeide Xavier / Matheus Silva
- **Estado:** **CONFIRMADO como registro de intenção** (2026-08-31)
- **Decisão fechada:** a **agenda geral da operação** será a fonte futura, com modelo específico:
  o **sistema interno planejado** (que substituirá a Kenlo) será a **fonte de verdade** — onde
  ficam as regras de negócio, bloqueio manual e confirmação do SDR já definidas nesta fase. O
  **Google Calendar** entra apenas como **camada de sincronização/visualização para os
  corretores**, não como sistema principal.
- **Natureza:** registro de intenção, **sem compromisso técnico** agora; a definição final e a
  integração de fato acontecem na Fase 3 (após fonte de agenda aprovada).
- **Impacto:** nesta fase o pedido continua como pendência no painel (RN-1, sem reserva);
  estrutura compatível com a fonte futura quando a Fase 3 integrar.

### 6. Dono do próximo passo

- **Dono:** Janeide Xavier / SDR
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:**
  - **SDR** é o dono do próximo passo para os estados `Pendente de agenda` e
    `Precisa esclarecer` — retoma a pendência e registra próximo passo com **ator e horário**
    (RN-4);
  - **gestor/Admin** corrige com **motivo e auditoria** (mesma lógica do painel);
  - pedidos **`Cancelado`** ficam **encerrados, sem próximo passo ativo** — apenas com
    `cancel_reason` registrado.

## Regras de negócio a validar no contrato

- **RN-1 — Sem reserva:** todo pedido da Fase 1 fica `Pendente de agenda`; nenhuma ação bloqueia
  slot/corretor/chave. Estados: `Pendente de agenda`, `Precisa esclarecer`, `Cancelado`.
- **RN-2 — Vínculo obrigatório:** pedido ligado a lead **e** imóvel; se faltar um → `Precisa esclarecer`.
- **RN-3 — Janela honesta:** salvar data/janela estruturada **ou** texto livre; ausência vira pendência.
- **RN-4 — Histórico:** edição/cancelamento registra ator, horário e motivo; não apaga histórico.
- **RN-5 — Texto e PII mínimos:** preferência em texto livre tratada como dado, limitada e escapada;
  conteúdo indevido/PII excedente vira pendência.

## Fixture de teste

O fixture `visita-001` será validado quando o ambiente for confirmado. Não contém PII real.

## Próximo passo

Realizar a **call de setup** com Matheus Silva (e Janeide Xavier quando aplicável) para fechar os
itens 1, 2, 5 e 6 (itens 3 e 4 já confirmados). Cada decisão fechada deve ser registrada neste
documento e no `changelog.md`. Itens não resolvidos permanecem como bloqueio em `STATUS.md`.