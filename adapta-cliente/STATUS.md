# STATUS — Projeto Imobiliária Janeide Xavier LTDA

> **Atualizado em:** 2026-09-22 · **Por:** Janeidinha

## Onde estamos

- **Fase atual:** Fase 2 — catálogo e atendimento consultivo.
- **Fase 1:** encerrada em 16/16 tasks; arquivo resumido em `05_entregas/fase-1/` e histórico completo preservado no Git.
- **Progresso Fase 2:** **1/8 tasks concluídas**; F2-T01 concluída após validação automática e teste humano aprovado.
- **Task ativa:** nenhuma; F2-T02 é a próxima task elegível, mas não foi iniciada nem autorizada.

## Objetivo

Catálogo versionado, busca por código/bairro/tipo, ficha vigente, card com envio humano rastreável, histórico, próximo passo e handoff, sem presumir API Kenlo, agenda ou classificação autônoma.

## Gates

- **F2-T01 — concluída (2026-09-22):** contrato da carga formalizado; fixture sintética, validador, recibo e relatório aprovados. B2-01, B2-02 e B2-04 confirmados por Janeide; nenhum catálogo real promovido.
- **F2-T02 — bloqueada:** depende do aceite da F2-T01 (agora atendido), de resolução/prova de B2-03 e de nova autorização explícita. Não iniciar automaticamente.
- Somente uma task por vez; autorização e teste humano antes das transições.
- `META_APP_SECRET` real é gate separado de produção.
- Skip 55154 não é acessível à conta de auditoria; tasks devem produzir evidência exportável ou acesso autorizado.
- **Changelog canônico:** a cópia local `adapta-cliente/changelog.md` permanece canônica; após o fechamento da F2-T01, o blob local atual é `81b01b1c51cfcd3029a6fda7034dfe8d3ffbf998`. O remoto pode continuar divergente em bytes porque o conector MCP do GitHub introduz drift de transcrição em arquivos longos. É limitação conhecida de publicação, não erro de conteúdo.
- A divergência de bytes do changelog não bloqueia a validação técnica; o drift está registrado no aprendizado contínuo.

## Decisões B2 registradas na F2-T01

- **B2-01:** exportação manual Kenlo em `.xls` com 29 colunas; zero monetário significa não preenchido; mídia não vem no arquivo e vira pendência de cadastro manual.
- **B2-02:** corte = data da exportação; frequência semanal; Matheus responsável pela exportação/carga; mais de seis meses sem atualização gera revisão, sem recusar o imóvel por isso.
- **B2-04:** retenção de um ano; log append-only por lote; histórico preservado; Promotor(es)/Indicador(es) fora do catálogo; Captador(es) apenas como campo interno de rastreabilidade.

## Evidência F2-T01

- Contrato: `04_fase-atual/setup/contrato-carga-fase-2.md`.
- Fixture: `04_fase-atual/fixtures/catalogo-f2-t01.json`.
- Validador: `04_fase-atual/scripts/validar-f2-t01.py`.
- Relatório/recibo: `06_notas/fase-2/relatorio-f2-t01.md` e `recibo-f2-t01.json`.
- Execução validada novamente no fechamento: 5 linhas — 2 aceitas, 1 pendente, 2 recusadas; `catalog_version` `cat-20260915-fac83f9cf10a`; `content_hash` `fac83f9cf10a55b9410066fd0061b28b36651131a7569f9ea67ebef6dd18c3cd`; 8 checagens PASS.
- Teste humano aprovado por Janeide Xavier em 2026-09-22: B2-01, B2-02 e B2-04 confirmados.
- Nenhum dado real, acesso ao Kenlo/Skip ou promoção de catálogo; F2-T02 não iniciada.
- Tentativa de patch documental: diff mínimo gerado entre o remoto e o local (`artifacts/changelog-local-vs-remote.patch`); a API GitHub disponível não oferece aplicação por hunk, e a canonicidade local foi mantida.

## Fora da fase

API Kenlo não comprovada, envio automático de WhatsApp, agenda/reserva, classificação autônoma, no-show e go-live.
