> **Atualizado em:** 2026-09-03 · **Por:** Janeidinha
> O painel do projeto: fase atual, progresso e o que precisa de atenção.

## Onde estamos

- **Fase atual:** Fase 1 — primeira vertical de atendimento · aberta documentalmente em 2026-08-17 · reunião de fechamento a agendar
- **Objetivo desta fase:** capturar lead com origem, organizar fila/contexto, consultar ficha vigente e registrar pedido de visita sem reserva automática.
- **No prazo?** em risco — fonte, permissões, plataforma, catálogo e ambiente de testes ainda não validados.

## Progresso da fase

- **Tasks:** 8/16 (50%) — F1-T01 a F1-T08 concluídas (leva 1 completa + levas 2, 3, 4 e 5 do caminho principal). F1-T06: fila + cartão mínimo de lead aprovada. F1-T07: consulta por código e preview de ficha aprovada. F1-T08: registro de pedido pendente sem agenda aprovada — dedupe (mesma janela não duplica), máscara de digitação, `Precisa esclarecer` com janela vazia, cancelamento com motivo.
- **Próxima task:** F1-T09 — exercitar bordas da captura e fila de pendência (SPEC-1-001), após F1-T05.

## Pendências de produção

| Pendência | Responsável | Quando resolver |
|---|---|---|
| Trocar `META_APP_SECRET` (teste fictício) pelo **App Secret real da Meta** no Skip Cloud | Matheus Silva | **Antes de publicar** o projeto em produção |

## Travas ativas

| Trava | Desde | Quem resolve | Ação em curso |
|---|---|---|---|
| Fonte e permissão de WhatsApp/CRM/webhook/dedupe | 2026-08-17 | Janeide/Matheus | validar fonte, campos e `capture_event_id` |
| Plataforma, armazenamento e papéis do painel | 2026-08-17 | Matheus/Janeide | contrato-painel.md: 6/6 itens confirmados (hospedagem Skip Cloud, retenção, modelo Lead, chave única, matriz de acesso, ambiente de teste dedicado) |
| Fonte do catálogo, vigência e mídia | 2026-08-17 | Matheus | contrato-catalogo.md criado (6 itens); confirmar Kenlo como fonte única e fechar vigência/mídia |
| Modelo de pedido, janela e timezone | 2026-08-17 | Janeide/SDR | contrato-pedido-visita.md criado; janela (agenda geral/texto livre) e timezone (America/Bahia) confirmados; fechar itens 1/2/5/6 |
| Ambiente de teste e evidências | 2026-08-17 | Matheus/Adapta | preparar fixtures e logs sem PII |

## Entregas concluídas

| Fase | O que foi entregue | Fechada em |
|---|---|---|
| — | Nenhuma fase concluída; Fase 1 está em preparação bloqueada | — |

## Próxima reunião

A agendar — call de setup com Matheus Silva e Janeide Xavier para fechar os itens dos contratos de setup já criados:

**Contrato de captura (F1-T01)** — 7 itens: fonte WhatsApp, CRM, mecanismo, campos, permissões, idempotência (`capture_event_id`) e ambiente de teste.

**Contrato de painel (F1-T02)** — 6 itens: superfície/plataforma, armazenamento/retenção, modelo Lead, chave única, matriz de acesso por papel e ambiente de teste.

**Contrato de catálogo (F1-T03)** — 6 itens: fonte de verdade (Kenlo Mob), acesso de leitura, campos mínimos, vigência/validade, mídia/envio por WhatsApp e responsável pela atualização do catálogo.

**Contrato de pedido de visita (F1-T04)** — 6 itens: modelo de pedido e estados, campos do pedido, janela estruturada vs. texto livre, timezone, fonte futura de agenda e dono do próximo passo. Janela e timezone (America/Bahia) já confirmados por Janeide; itens 1/2/5/6 aguardam call de setup.