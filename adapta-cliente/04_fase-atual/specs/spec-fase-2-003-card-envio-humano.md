# SPEC-2-003 — Card e envio humano rastreável

**Fase:** 2  
**Status:** bloqueada pelas SPEC-2-001/002  
**Dono:** SDR + Champion  
**Origem:** RQ-002/RQ-003/RQ-008/RQ-010; C2; decisão F1 de envio manual  
**Degrau:** reuso + construção mínima — reutilizar preview/vínculo da F1 e completar card, galeria permitida e histórico, sem automatizar o WhatsApp.

## Contexto e decisões fechadas

- **Atual:** F1 provou preview por código e registro de envio humano com `message_ref` quando disponível.
- **Desejado:** o SDR monta/revisa card a partir da versão ativa, envia manualmente pelo canal atual e registra exatamente um vínculo reproduzível entre lead, imóvel, versão, usuário e horário.
- **Fechado:** nenhum envio automático; número atual/app comum; somente mídia da fonte/allowlist; negociação permanece humana.
- **Bloqueios:** versão/ficha aceitas; B2-04 política de PII/log; B2-06 forma disponível de referência do envio.

## Resultado observável

Para uma ficha vigente, o SDR vê um card revisável, confirma a ação humana e registra o envio. Repetição não cria segundo vínculo; card desatualizado ou inválido é recusado com motivo.

## Limites e dependências

- **Inclui:** composição determinística, preview, confirmação humana, cópia/abertura manual, registro de envio, dedupe, histórico e revogação lógica do card.
- **Fora:** Cloud API, disparo automático, chatbot, copy gerada, negociação, tracking de leitura não disponível.
- **Entradas:** lead autorizado, ficha/versão aceita, usuário SDR e canal manual.
- **Saídas:** `card_version`, `send_intent_id`, `message_ref` opcional, vínculo e recibo.
- **Permissões:** SDR atribuído registra; gestor audita; ator não atribuído não vê PII/histórico.
- **Superfícies:** preview/card no painel F1, registro de intenção/recibo de envio e histórico do lead; sem superfície de disparo automático.
- **Risco/plano B:** sem `message_ref`, registrar recibo manual mínimo com `send_intent_id`, usuário, timestamp e confirmação; nunca inventar ID externo.
- **Rollback:** suspender novos cards e manter ficha/registro manual; histórico existente não é apagado.

## Dados e regras

| Regra | Condição | Resultado | Exceção |
|---|---|---|---|
| RN-221 | ficha ativa e vigente | card deriva exatamente da versão | edição livre não altera a fonte |
| RN-222 | confirmação humana ausente | nenhum envio/vínculo concluído | preview pode existir |
| RN-223 | `message_ref` indisponível | recibo manual explícito | campo fica ausente, nunca fictício |
| RN-224 | retry com a mesma `send_intent_id` | um vínculo, retorno idempotente | “novo envio” consciente cria nova intenção e novo vínculo, mesmo para o mesmo card |
| RN-225 | card ficou vencido/inativo entre preview e confirmação | recusar confirmação e pedir nova revisão | sem envio silencioso |
| RN-226 | mídia insegura | bloquear card/arquivo correspondente | link textual só permanece após aprovação do responsável de cadastro/gestor |

## Fluxo e recuperação

1. Abrir lead atribuído e selecionar ficha vigente.
2. Gerar preview com versão/fonte.
3. Revalidar vigência imediatamente antes da confirmação.
4. SDR confirma e realiza envio fora do sistema pelo canal atual.
5. Registrar recibo/vínculo; repetição retorna o original.
6. Falha ou abandono mantém intenção pendente, nunca “enviado”.

## Instruções para o Ethos

1. Ler SPEC-2-001/002 e contrato F1-T03.
2. Alterar apenas card, confirmação e histórico de envio.
3. Não integrar WhatsApp, disparar mensagem, inventar `message_ref` ou expor PII.
4. Executar preview → revalidação → confirmação → recibo → repetição → card vencido.
5. Parar se política de PII ou papel atribuído não estiver aplicável.
6. Preservar consulta e envio manual da F1.

## Checklist

- [ ] card deriva da versão ativa;
- [ ] confirmação humana obrigatória;
- [ ] fallback sem `message_ref` explícito;
- [ ] idempotência e card vencido testados;
- [ ] permissão negativa testada;
- [ ] aceite SDR registrado.

## Critérios de aceite

- [ ] **CA-2-013:** preview identifica lead, imóvel, fonte e `card_version` sem alterar dados da fonte.
- [ ] **CA-2-014:** nenhuma ação é registrada como enviada antes da confirmação humana do SDR.
- [ ] **CA-2-015:** envio manual confirmado gera um único recibo com ator e horário; `message_ref` só existe quando observado.
- [ ] **CA-2-016:** repetição da mesma intenção não cria segundo vínculo nem segundo estado “enviado”.
- [ ] **CA-2-017:** ficha vencida/inativa ou mídia insegura entre preview e confirmação bloqueia o card com motivo.
- [ ] **CA-2-018:** usuário não atribuído não acessa PII nem registra envio no lead.

## TDD da SPEC

| Etapa | Prova | Ação | Esperado | Evidência |
|---|---|---|---|---|
| RED | preview atual + envio manual | procurar recibo completo | vínculo F2 ainda incompleto | relatório RED |
| GREEN | ficha/lead sintéticos | preview, confirmar e repetir | CA-2-013..016 passam | recibos + histórico |
| REGRESSÃO | vencer card + mídia insegura + usuário não atribuído | confirmar/acessar | bloqueios e 403/negação | logs sanitizados |

**Fixtures:** lead e imóvel sintéticos; nenhum telefone real.  
**Evidência:** preview, recibo, histórico, prova idempotente, bloqueios e aceite humano.

## Handoff e operação

- **Demonstrar:** abrir lead, revisar card, confirmar envio manual e abrir recibo.
- **Operar:** SDR envia; cadastro corrige catálogo; gestor revisa exceções.
- **Monitorar:** intenções pendentes, duplicidades evitadas, cards vencidos e negações.

## Tasks vinculadas

| ID | Task | Dono | SPEC | Critério | Recorte da prova | Evidência esperada | Pré-condições | Status |
|---|---|---|---|---|---|---|---|---|
| F2-T05 | Implementar card consistente e confirmação de envio humano | Ethos | SPEC-2-003 | CA-2-013 a CA-2-015 | GREEN ficha→card→registro, sem envio automático | card, comparação com ficha e vínculo de envio | F2-T04 aceita; B2-04 aplicado; B2-06 definido ou fallback interno | BLOQUEADA |
| F2-T06 | Provar dedupe, mudança de versão, mídia insegura e log sanitizado | Ethos | SPEC-2-003 | CA-2-016 a CA-2-018 | REGRESSÃO com retry, versão alterada, vencimento, mídia insegura e canal sem ID | relatório, vínculo idempotente e scan de segredos | F2-T05 aceita | BLOQUEADA |

## Emendas

| Data | Origem | Micro-spec/task | Motivo |
|---|---|---|---|
