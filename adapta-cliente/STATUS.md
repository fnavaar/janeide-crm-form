# STATUS — Projeto Imobiliária Janeide Xavier LTDA

> **Atualizado em:** 2026-09-28 · **Por:** Janeidinha

## Onde estamos

- **Fase atual:** Fase 2 — catálogo e atendimento consultivo.
- **Fase 1:** encerrada em 16/16 tasks; arquivo resumido em `05_entregas/fase-1/` e histórico completo preservado no Git.
- **Progresso Fase 2:** **1/8 tasks concluídas**; F2-T01 concluída e F2-T02 em implementação autorizada.
- **Task ativa:** F2-T02 — carga versionada, idempotência, promoção controlada e rollback lógico no Skip 55154; não iniciar F2-T03.

## Objetivo

Catálogo versionado, busca por código/bairro/tipo, ficha vigente, card com envio humano rastreável, histórico, próximo passo e handoff, sem presumir API Kenlo, agenda ou classificação autônoma.

## Gates

- **F2-T01 — concluída (2026-09-22):** contrato da carga formalizado; fixture sintética, validador, recibo e relatório aprovados. B2-01, B2-02 e B2-04 confirmados por Matheus Silva; nenhum catálogo real promovido.
- **F2-T02 — aguardando teste humano:** causa raiz da falha de importação V1 confirmada e corrigida. O campo booleano `stale_review` aceitava `true`, mas `false` falhava porque estava marcado como obrigatório; recibos de falha também precisavam aceitar `accepted=0`/`pending=0`. Migrations 0028/0029 aplicadas. QA Skip 0.0.75 PASS (setup, análise estática, build, integrações e testes); suíte sintética runtime 19/19 PASS: hash/totais V1 corretos, idempotência e duplicata por conteúdo, promoção V1, falha parcial atômica preservando V1, V2 sintética distinta, promoção V2, rollback V2→V1 e login/leitura/403 para SDR e Corretor. V1 permanece ativa; teste humano da UI e regressão da Fase 1 ainda pendentes. Projeto 55154 não publicado; rotas diagnósticas retornam 404 e secrets temporários foram removidos. Não iniciar F2-T03.
- Somente uma task por vez; autorização e teste humano antes das transições.
- `META_APP_SECRET` real é gate separado de produção.
- Projeto Skip 55154 é o ambiente de teste não publicado; a conta técnica dedicada foi provisionada para prova independente, sem acesso a produção e sem carga de dados reais de cliente.
- **B2-03/F2-T02 — decisões fechadas:** autoridade exclusiva = papel Admin (Matheus é o ocupante atual, sem amarrar o contrato à pessoa); SDR/Corretor somente leitura. A conta Auditoria F2-T02 é exclusiva do Skip 55154 para provas sintéticas, não é autoridade de negócio e deve ser removida/desativada antes de produção.
- **Escopo F2-T02:** fixture sintética apenas; Skip 55154; sequência V1 → V2 sintética alterada → rollback V2→V1. Exportação `.xls` real fica fora desta task e exige autorização própria. Implementação autorizada; parada em teste humano; F2-T03 não iniciada.
- **B2-01:** exportação manual Kenlo em `.xls` com 29 colunas; zero monetário significa não preenchido; mídia não vem no arquivo e vira pendência de cadastro manual.
- **B2-02:** corte = data da exportação; frequência semanal; Matheus responsável pela exportação/carga; mais de seis meses sem atualização gera revisão, sem recusar o imóvel por isso.
- **B2-04:** retenção de um ano; log append-only por lote; histórico preservado; Promotor(es)/Indicador(es) fora do catálogo; Captador(es) apenas como campo interno de rastreabilidade.
- **Changelog canônico:** a cópia local `adapta-cliente/changelog.md` permanece canônica; após o registro de B2-03 e a correção de autoria do fechamento da F2-T01, o blob local atual é `d236546f2377c6541a37a301be470c7ae944490c`. O remoto pode continuar divergente em bytes porque o conector MCP do GitHub introduz drift de transcrição em arquivos longos. É limitação conhecida de publicação, não erro de conteúdo.
- A divergência de bytes do changelog não bloqueia a validação técnica; o drift está registrado no aprendizado contínuo.

## Evidência F2-T01

- Contrato: `04_fase-atual/setup/contrato-carga-fase-2.md`.
- Fixture: `04_fase-atual/fixtures/catalogo-f2-t01.json`.
- Validador: `04_fase-atual/scripts/validar-f2-t01.py`.
- Relatório/recibo: `06_notas/fase-2/relatorio-f2-t01.md` e `recibo-f2-t01.json`.
- Execução validada novamente no fechamento: 5 linhas — 2 aceitas, 1 pendente, 2 recusadas; `catalog_version` `cat-20260915-fac83f9cf10a`; `content_hash` `fac83f9cf10a55b9410066fd0061b28b36651131a7569f9ea67ebef6dd18c3cd`; 8 checagens PASS.
- Teste humano aprovado por Matheus Silva em 2026-09-22: B2-01, B2-02 e B2-04 confirmados.
- **F2-T02:** somente fixtures sintéticas no Skip 55154; implementação autorizada em 2026-09-28. Prova obrigatória V1→V2 sintética alterada→rollback V2→V1; Admin promove/corrige/rollback, SDR/Corretor somente leitura. Não importar `.xls` real e não iniciar F2-T03.
- Tentativa de patch documental: diff mínimo gerado entre o remoto e o local (`artifacts/changelog-local-vs-remote.patch`); a API GitHub disponível não oferece aplicação por hunk, e a canonicidade local foi mantida.

## Fora da fase

API Kenlo não comprovada, envio automático de WhatsApp, agenda/reserva, classificação autônoma, no-show e go-live.
