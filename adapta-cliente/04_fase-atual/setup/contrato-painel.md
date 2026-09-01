# Contrato de Setup — Painel de Lead e Contexto Consultivo (F1-T02)

**Task:** F1-T02 — Fechar superfície do painel, modelo Lead e matriz de acesso
**SPEC:** SPEC-1-002
**Dono:** Matheus Silva
**Criado em:** 2026-08-26 por Janeidinha
**Estado:** CONFIRMADO — todos os 6 itens fechados (superfície/hospedagem Skip Cloud, armazenamento/retenção, modelo Lead, chave única, matriz de acesso, ambiente de teste dedicado)

> Este documento registra as decisões que precisam ser fechadas para destravar a leva 4 da Fase 1
> (F1-T06). Cada item tem dono, estado e o que precisa para fechar. Nenhum item pode ser presumido
> ou inventado — ausência de decisão vira bloqueio registrado. Replica o padrão do
> `contrato-captura.md` (F1-T01).

## Itens de decisão

### 1. Superfície / plataforma do painel

- **Dono:** Matheus Silva / Adapta
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** seguir com o **Skip Cloud** como plataforma de hospedagem do painel
  (stack já provisionada, evita segundo provedor). Porta de saída confirmada para migração
  futura: exportação de **código-fonte** + banco **PocketBase** exportável.
- **Impacto:** painel hospedado na Skip Cloud (URL pública `goskip.app`); sem servidor separado;
  migração futura possível via código-fonte + banco PocketBase.

### 2. Armazenamento e retenção

- **Dono:** Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-27)
- **Decisão fechada:** retenção **indefinida**, com **consentimento explícito de retenção longa**
  coletado no formulário.
- **Impacto:** cartões/eventos persistidos indefinidamente; exigência de consentimento explícito
  de retenção longa (LGPD) registrado no formulário de captura.

### 3. Modelo Lead / campos

- **Dono:** Janeide Xavier / Matheus Silva
- **Estado:** **CONFIRMADO** (2026-08-27)
- **Decisão fechada:** modelo de Lead com **15 campos**, mantendo `property_code` (quando o lead
  vem de imóvel específico) e adicionando **perfil de busca — bairro, tipo, quartos, valor** —
  para quando o lead não vem de imóvel específico, podendo os dois coexistir. **Nome e telefone
  ficam diretos no cartão**, não como referência.
- **Impacto:** cartão exibe nome e telefone diretos; `property_code` opcional conforme a origem;
  entram campos de perfil de busca; **datas de primeiro e último contato separadas** no cartão
  (gravadas na captura: primeira cria, seguintes atualizam último contato); a lista fechada dos
  15 campos e seus formatos será revisada na call de setup.

### 4. Chave única do lead

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-27)
- **Decisão fechada:** `lead_id` como chave única, formato **UUID gerado no primeiro contato do
  lead** — não derivado de `capture_event_id` (isso quebraria o dedupe por telefone/e-mail).
  Fluxo: toda captura passa primeiro pelo **dedupe por telefone ou e-mail**; se encontrar lead
  existente, reutiliza o `lead_id`; se não, gera UUID novo. `capture_event_id` fica registrado
  como **referência do evento**, vinculado ao `lead_id`, sem ser a fonte da chave.
- **Impacto:** garante um cartão por pessoa (RN-1) mesmo com múltiplas capturas; idempotência
  por telefone/e-mail preservada; `capture_event_id` mantido como referência de evento.

### 5. Matriz de acesso por papel

- **Dono:** Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-27)
- **Decisão fechada — papéis:** **SDR, Corretor, Admin**.
  - **SDR:** vê telefone completo de **todos** os leads.
  - **Corretor:** vê telefone completo **somente do lead atribuído a ele** — não dos leads de
    outros corretores.
  - **Admin:** vê telefone completo de **todos** os leads (acesso de emergência).
  - **Demais papéis** (estagiário, marketing, financeiro etc.): **sem acesso a telefone**.
- **Impacto:** regra de privacidade por papel (RN-4) aplicada ao telefone; o sistema deve
  ocultar/bloquear o campo para papéis não autorizados. Origem imutável pelo SDR (RN-3);
  correção exige gestor/Admin, motivo e auditoria.

### 6. Ambiente de teste

- **Dono:** Matheus Silva / Adapta
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** criar um **projeto Skip dedicado, novo, exclusivo para testes**. Não
  reaproveitar "Gestão Imobiliária" (tem erros conhecidos; não é candidato a produção neste
  momento — fica separado para revisão posterior) nem "Página de Formulário" (escopo diferente,
  só formulário).
- **Impacto:** fixtures (`cap-001`, `lead-001`, `imovel-001`, `visita-001`) executados em
  ambiente Skip isolado com dados fictícios, sem misturar com produção. A criação efetiva do
  projeto de teste acontece na implementação da leva 2 (F1-T05).

## Regras de negócio a validar no contrato

- **RN-1 — Uma entrada:** um cartão por `lead_id`; conflito de chave vira pendência.
- **RN-3 — Origem protegida:** origem não pode ser editada pelo SDR; correção exige gestor, motivo
  e auditoria.
- **RN-4 — Privacidade por papel:** mostrar somente campos permitidos; permissão negada não revela
  valor.
- **RN-5 — Texto operacional:** próximo passo/pendência é texto, escapar apresentação e nunca
  executar conteúdo.

## Fixture de teste

O fixture `lead-001` será validado quando o ambiente for confirmado. Não contém PII real.

## Próximo passo

Realizar a **call de setup** com Matheus Silva (e Janeide Xavier quando aplicável) para fechar os
itens acima. Cada decisão fechada deve ser registrada neste documento e no `changelog.md`.
Itens não resolvidos permanecem como bloqueio registrado em `STATUS.md`.