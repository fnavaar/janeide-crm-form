# Fase 1 — Tarefas gerais

**Status:** leva 1 concluída (F1-T01 a F1-T04 com contratos de setup e fixtures); demais tasks bloqueadas por pré-condições.  
**Fonte:** `01-SPECs/` e `matriz-de-rastreabilidade.md`  
**Regra:** executar uma task por vez; não resolver BLOQUEIO inventando fonte, acesso, arquitetura ou aceite.

## Tasks

| ID | Leva | Task | Dono | SPEC | Critério binário | Recorte da prova | Evidência esperada | Pré-condições | Ponto de parada | Status |
|---|---:|---|---|---|---|---|---|---|---|---|
| F1-T01 | 1 | Fechar contrato de captura, origem, webhook, CRM e dedupe | Matheus Silva | SPEC-1-001 | fonte, campos, permissão e `capture_event_id` aprovados ou bloqueio registrado | Contexto; Dados e integrações; Instruções 1–5 | decisão/registro de setup e fixture `cap-001` | call de setup | parar sem implementar se fonte/chave não forem aprovadas | CONCLUÍDA 2026-08-18 |
| F1-T02 | 1 | Fechar superfície do painel, modelo Lead e matriz de acesso | Matheus Silva | SPEC-1-002 | plataforma, armazenamento, campos e papéis SDR/gestor aprovados | Contexto; Dados; Checklist | mapa de campos, papéis e ambiente | call de setup | parar se houver PII/campo/retensão sem dono | CONCLUÍDA 2026-08-26 |
| F1-T03 | 1 | Fechar fonte do catálogo, campos, vigência e mídia | Matheus Silva | SPEC-1-003 | fonte única, status, validade, campos e mídia aprovados | Contexto; Dados; Regras RN-1–RN-5 | contrato de catálogo e imóvel de teste | call de setup | parar se Kenlo/site ou vigência divergirem | CONCLUÍDA 2026-08-26 |
| F1-T04 | 1 | Fechar modelo do pedido de visita e regra de não reserva | Janeide Xavier | SPEC-1-004 | estados, janela, timezone e dono do próximo passo aprovados | Contexto; Dados; Regras RN-1–RN-5 | decisão operacional e exemplo sem booking | call de setup | parar se a Fase 1 for solicitada a reservar horário | CONCLUÍDA 2026-08-26 |
| F1-T05 | 2 | Configurar link e captura idempotente de lead | Matheus Silva | SPEC-1-001 | evento válido cria/atualiza um lead com origem e código | Resultado; Fluxo 1–5; CA-1-01/02 | ID do lead, log e captura | F1-T01; acesso aprovado | parar em evento sem ID, CRM ou permissão | CONCLUÍDA 2026-09-01 |
| F1-T06 | 3 | Configurar fila e cartão mínimo de lead | Matheus Silva | SPEC-1-002 | lead válido aparece uma vez com origem, estado e contexto | Resultado; Fluxo 1–6; CA-1-05/06 | captura do cartão e auditoria | F1-T02 e F1-T05 | parar se campo ou papel não estiver autorizado | CONCLUÍDA 2026-09-03 |
| F1-T07 | 4 | Configurar consulta por código e preview de ficha | Matheus Silva | SPEC-1-003 | código ativo retorna preview com fonte/vigência sem preencher ausências | Resultado; Fluxo 1–3; CA-1-09/11 | preview, `source_ref` e bloqueio | F1-T03 e F1-T06 | parar em fonte vencida, campo ausente ou mídia insegura | CONCLUÍDA 2026-09-03 |
| F1-T08 | 5 | Configurar registro de pedido pendente sem agenda | SDR | SPEC-1-004 | pedido vinculado recebe `Pendente de agenda` e próximo passo | Resultado; Fluxo 1–5; CA-1-13/14 | ID do pedido e cartão | F1-T04 e F1-T06/F1-T07 | parar se surgir slot, corretor, chave ou reserva | CONCLUÍDA 2026-09-03 |
| F1-T09 | 6 | Exercitar bordas da captura e fila de pendência | Matheus Silva | SPEC-1-001 | inválido, repetido, opt-out e indisponível geram resultado correto | Cenários; RN-1–RN-5; caminhos de erro | relatório de quatro cenários | F1-T05 | parar em sucesso falso, duplicidade ou PII em log | CONCLUÍDA 2026-09-04 |
| F1-T10 | 6 | Exercitar permissões, auditoria e dados incompletos do painel | Matheus Silva | SPEC-1-002 | acesso negado, lead incompleto e painel indisponível são recuperáveis | Cenários; RN-3–RN-5 | log de acesso, pendência e sem vazamento | F1-T06 | parar em alteração indevida ou cartão falso | BLOQUEADA |
| F1-T11 | 6 | Exercitar bloqueios de catálogo, mídia e envio duplicado | Matheus Silva | SPEC-1-003 | inativo, incompleto, divergente, URL insegura e retry bloqueiam corretamente | Cenários; RN-1–RN-5 | relatório e logs de bloqueio | F1-T07 | parar se dado não confirmado for enviado | BLOQUEADA |
| F1-T12 | 6 | Exercitar janela incompleta, duplicidade e tentativa de booking | SDR | SPEC-1-004 | pedido incompleto esclarece; repetição não duplica; booking é bloqueado | Cenários; RN-1–RN-5 | pedido, log e bloqueio de reserva | F1-T08 | parar se pedido for tratado como agendado | BLOQUEADA |
| F1-T13 | 7 | Demonstrar captura ponta a ponta e handoff ao SDR | SDR | SPEC-1-001 | CA-1-01 a CA-1-04 passam no fixture aprovado | TDD RED/GREEN/REGRESSÃO; Handoff | vídeo/capturas, logs e aceite SDR/Matheus | F1-T09 | parar e devolver à SPEC se qualquer CA falhar | BLOQUEADA |
| F1-T14 | 7 | Demonstrar fila, próximo passo e auditoria do lead | SDR | SPEC-1-002 | CA-1-05 a CA-1-08 passam sem vazamento | TDD; Handoff | captura, log e aceite SDR | F1-T10 | parar e devolver à SPEC se qualquer CA falhar | BLOQUEADA |
| F1-T15 | 7 | Demonstrar ficha vigente e envio humano rastreável | SDR | SPEC-1-003 | CA-1-09 a CA-1-12 passam sem dado inventado/duplicidade | TDD; Handoff | preview, `message_ref`, vínculo e aceite | F1-T11 | parar e devolver à SPEC se qualquer CA falhar | BLOQUEADA |
| F1-T16 | 7 | Demonstrar pedido pendente e handoff para Fase 3 | SDR | SPEC-1-004 | CA-1-13 a CA-1-16 passam sem reserva | TDD; Handoff | pedido, estado, bloqueio e aceite | F1-T12 | parar e devolver à SPEC se qualquer CA falhar | BLOQUEADA |

## Dependências de execução

- A leva 1 é independente entre as quatro SPECs e deve ser resolvida com os responsáveis indicados.
- As levas 2–5 formam o caminho principal em ordem topológica; cada task só é liberada depois de
  todas as pré-condições listadas estarem concluídas.
- As quatro tasks da leva 6 são independentes entre si após o caminho principal correspondente;
  as quatro da leva 7 também são independentes entre si após suas bordas passarem.
- Tasks bloqueadas não autorizam implementação parcial; o ponto de parada é parte do contrato.