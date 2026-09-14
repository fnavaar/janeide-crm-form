# STATUS — Projeto Imobiliária Janeide Xavier LTDA

> **Atualizado em:** 2026-09-14 · **Por:** Janeidinha
> O painel do projeto: fase atual, progresso e o que precisa de atenção.

## Onde estamos

- **Fase atual:** Fase 1 — primeira vertical de atendimento · checklist completo em 2026-09-10 · validação final do consultor pendente
- **Objetivo desta fase:** capturar lead com origem, organizar fila/contexto, consultar ficha vigente e registrar pedido de visita sem reserva automática.
- **Situação:** execução, testes humanos e sincronização documental da Fase 1 concluídos em 2026-09-14; validação final do consultor pendente.

## Progresso da fase

- **Tasks:** 16/16 (100%) — F1-T01 a F1-T16 concluídas. F1-T15: ficha vigente, envio humano rastreável, repetição sem segundo vínculo e 4 bloqueios aprovados manualmente. F1-T16: pedido com janela estruturada pendente, repetição sem segundo registro, texto livre em `Precisa esclarecer`, ausência de booking e cancelamento com motivo/histórico aprovados manualmente.
- **Próxima etapa:** obter a validação final do consultor sobre o conteúdo publicado no GitHub antes de considerar a Fase 1 formalmente encerrada.

## Pendências de produção

| Pendência | Responsável | Quando resolver |
|---|---|---|
| Trocar `META_APP_SECRET` pelo **App Secret real da Meta** no Skip Cloud (valor de teste já rotacionado em 2026-09-04) | Matheus Silva | **Antes de publicar** o projeto em produção |

## Pendências de encerramento

| Pendência | Responsável | Quando resolver |
|---|---|---|
| Confirmar leitura e validação final do conteúdo da Fase 1 no GitHub | Consultor / Matheus Silva | Após a sincronização — **sincronização byte a byte concluída em 2026-09-14** (changelog.md corrigido no commit `4f73921`, blob SHA remoto == local, confirmado por leitura de volta) |

## Entregas concluídas

| Fase | O que foi entregue | Fechada em |
|---|---|---|
| Fase 1 | Checklist funcional completo: captura, fila, catálogo, pedido de visita, bordas e demonstrações ponta a ponta; validação final do consultor pendente | Aguardando validação final |

## Próxima reunião

A agendar — validação final do consultor com Matheus Silva e Janeide Xavier, após a sincronização do conteúdo local para o GitHub.

**Evidências a revisar:**

- F1-T01 a F1-T04: contratos de captura, painel, catálogo e pedido de visita confirmados.
- F1-T05 a F1-T12: captura idempotente, fila, ficha, pedido sem reserva e cenários de borda verificados.
- F1-T13 a F1-T16: demonstrações ponta a ponta, permissões, ficha vigente/envio rastreável e handoff sem booking aprovados manualmente.
- Pendência separada de produção: substituir o `META_APP_SECRET` de teste pelo valor real da Meta antes de publicar em produção.
