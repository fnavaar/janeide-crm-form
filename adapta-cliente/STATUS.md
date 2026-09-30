# STATUS — Projeto Imobiliária Janeide Xavier LTDA

> **Atualizado em:** 2026-09-30 · **Por:** Janeidinha

## Onde estamos

- **Fase atual:** Fase 2 — catálogo e atendimento consultivo.
- **Fase 1:** encerrada em 16/16 tasks; arquivo resumido em `05_entregas/fase-1/` e histórico completo preservado no Git.
- **Progresso Fase 2:** **1/8 tasks concluídas**; F2-T01 concluída e F2-T02 aguardando validação humana após correção.
- **Task ativa:** F2-T02 — carga versionada, idempotência, promoção controlada e rollback lógico no Skip 55154; correção da duplicidade visual aplicada; continuar teste humano pelo Corretor; não iniciar F2-T03.

## Objetivo

Catálogo versionado, busca por código/bairro/tipo, ficha vigente, card com envio humano rastreável, histórico, próximo passo e handoff, sem presumir API Kenlo, agenda ou classificação autônoma.

## Gates

- **F2-T01 — concluída (2026-09-22):** contrato da carga formalizado; fixture sintética, validador, recibo e relatório aprovados. B2-01, B2-02 e B2-04 confirmados por Matheus Silva; nenhum catálogo real promovido.
- **F2-T02 — aguardando teste humano:** correção da duplicidade visual identificada no teste SDR: `src/pages/CatalogoF2T02.tsx` tinha dois cartões de bloqueio sob a mesma condição de papel; o segundo foi removido e o primeiro botão foi mantido. O SDR já obteve HTTP 403 esperado no build 0.0.75; A2 e A4 aprovados. QA/build Skip 0.0.76 (`d69136f`) PASS em setup/static/build/integrations/test; runtime backend 19/19 PASS previamente. Projeto 55154 continua não publicado. Próximo teste humano: Corretor deve ler V1 e 2 itens, ver apenas um cartão/botão e obter HTTP 403; depois conferir C e executar D. Não iniciar F2-T03. Janeide aceitou a pendência antiga `.skip.config.json` para o finalize; depois do QA, o Skip ainda a lista em `pendingChanges` e o arquivo atual registra `lastDevBuildRef: d69136f`; origem antiga é hipótese aceita para esta decisão, não diff confirmado.
- Somente uma task por vez; autorização e teste humano antes das transições.
- `META_APP_SECRET` real é gate separado de produção.
- Projeto Skip 55154 é o ambiente de teste não publicado; a conta técnica dedicada foi provisionada para prova independente, sem acesso a produção e sem carga de dados reais de cliente.
- **B2-03/F2-T02 — decisões fechadas:** autoridade exclusiva = papel Admin (Matheus é o ocupante atual, sem amarrar o contrato à pessoa); SDR/Corretor somente leitura. A conta Auditoria F2-T02 é exclusiva do Skip 55154 para provas sintéticas, não é autoridade de negócio e deve ser removida/desativada antes de produção.
- **Escopo F2-T02:** fixture sintética apenas; Skip 55154; sequência V1 → V2 sintética alterada → rollback V2→V1. Exportação `.xls` real fica fora desta task e exige autorização própria. Implementação autorizada; parada em teste humano; F2-T03 não iniciada.
- **B2-01:** exportação manual Kenlo em `.xls` com 29 colunas; zero monetário significa não preenchido; mídia não vem no arquivo e vira pendência de cadastro manual.
- **B2-02:** corte = data da exportação; frequência semanal; Matheus responsável pela exportação/carga; mais de seis meses sem atualização gera revisão, sem recusar o imóvel por isso.
- **B2-04:** retenção de um ano; log append-only por lote; histórico preservado; Promotor(es)/Indicador(es) fora do catálogo; Captador(es) apenas como campo interno de rastreabilidade.
- **Changelog canônico:** a cópia local `adapta-cliente/changelog.md` é a fonte canônica desta sincronização; hash Git blob local `c65eff9e4e29975b196794a4c687baa761b546e5`. A leitura de volta dos arquivos publicados será conferida por blob SHA, pois o conector pode introduzir drift de transcrição em arquivos longos.
- Não há divergência documental declarada após o checkpoint publicado de 2026-09-30; verificar hashes novamente nesta atualização.

## Evidência F2-T01

- Contrato: `04_fase-atual/setup/contrato-carga-fase-2.md`.
- Fixture: `04_fase-atual/fixtures/catalogo-f2-t01.json`.
- Validador: `04_fase-atual/scripts/validar-f2-t01.py`.
- Relatório/recibo: `06_notas/fase-2/relatorio-f2-t01.md` e `recibo-f2-t01.json`.
- Execução validada novamente no fechamento: 5 linhas — 2 aceitas, 1 pendente, 2 recusadas; `catalog_version` `cat-20260915-fac83f9cf10a`; `content_hash` `fac83f9cf10a55b9410066fd0061b28b36651131a7569f9ea67ebef6dd18c3cd`; 8 checagens PASS.
- Teste humano aprovado por Matheus Silva em 2026-09-22: B2-01, B2-02 e B2-04 confirmados.
- **F2-T02:** somente fixtures sintéticas no Skip 55154; prova V1→V2 sintética alterada→rollback V2→V1; Admin promove/corrige/rollback, SDR/Corretor somente leitura. Correção da UI feita em 0.0.76; seguir com teste humano do Corretor, depois C e D. Não importar `.xls` real nem iniciar F2-T03.
- Tentativa de patch documental: diff mínimo gerado entre o remoto e o local (`artifacts/changelog-local-vs-remote.patch`); a API GitHub disponível não oferece aplicação por hunk, e a canonicidade local foi mantida.

## Fora da fase

API Kenlo não comprovada, envio automático de WhatsApp, agenda/reserva, classificação autônoma, no-show e go-live.
