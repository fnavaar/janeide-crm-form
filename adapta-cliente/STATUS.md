# STATUS — Projeto Imobiliária Janeide Xavier LTDA

> **Atualizado em:** 2026-09-15 · **Por:** Janeidinha

## Onde estamos

- **Fase atual:** Fase 2 — catálogo e atendimento consultivo.
- **Fase 1:** encerrada em 16/16 tasks; arquivo resumido em `05_entregas/fase-1/` e histórico completo preservado no Git.
- **Progresso Fase 2:** 0/8 tasks concluídas; F2-T01 implementada documentalmente e aguardando aceite humano.
- **Task ativa:** F2-T01 — contrato da carga, fonte, vigência e política do catálogo.

## Objetivo

Catálogo versionado, busca por código/bairro/tipo, ficha vigente, card com envio humano rastreável, histórico, próximo passo e handoff, sem presumir API Kenlo, agenda ou classificação autônoma.

## Gates

- F2-T01: contrato, fixture sintética, validador, recibo `validation_only` e relatório gerados; aceite humano pendente.
- F2-T02 permanece bloqueada até o aceite da F2-T01 e resolução/prova de B2-03.
- Somente uma task por vez; teste humano antes da próxima.
- `META_APP_SECRET` real é gate separado de produção.
- Skip 55154 não é acessível à conta de auditoria; tasks devem produzir evidência exportável ou acesso autorizado.

## Decisões B2 registradas na F2-T01

- **B2-01:** exportação manual Kenlo em `.xls` com 29 colunas; zero monetário significa não preenchido; mídia não vem no arquivo e vira pendência de cadastro manual.
- **B2-02:** corte = data da exportação; frequência semanal; Matheus responsável pela exportação/carga; mais de seis meses sem atualização gera revisão, sem recusar o imóvel por isso.
- **B2-04:** retenção de um ano; log append-only por lote; histórico preservado; Promotor(es)/Indicador(es) fora do catálogo; Captador(es) apenas como campo interno de rastreabilidade.

## Evidência F2-T01

- Contrato: `04_fase-atual/setup/contrato-carga-fase-2.md`.
- Fixture: `04_fase-atual/fixtures/catalogo-f2-t01.json`.
- Validador: `04_fase-atual/scripts/validar-f2-t01.py`.
- Relatório/recibo: `06_notas/fase-2/relatorio-f2-t01.md` e `recibo-f2-t01.json`.
- Execução local: 5 linhas — 2 aceitas, 1 pendente, 2 recusadas; hash e versão determinísticos; nenhum dado real, acesso ao Kenlo/Skip ou promoção de catálogo.

## Fora da fase

API Kenlo não comprovada, envio automático de WhatsApp, agenda/reserva, classificação autônoma, no-show e go-live.
