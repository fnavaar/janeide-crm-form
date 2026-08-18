# SPEC-1-002 — painel mínimo de lead e contexto consultivo

**Fase:** 1  
**Status:** bloqueada  
**Dono:** SDR/gestor da operação, com execução técnica de Matheus Silva  
**Origem no escopo:** C1, C2 inicial, RQ-003, RQ-008, D-102  
**Degrau da solução:** construção mínima — uma fila/cartão operacional com os campos necessários, sem substituir o CRM ou construir ainda o catálogo completo.

## Contexto e decisões fechadas

- **Estado atual:** o atendimento alterna WhatsApp, site e CRM; o contexto e o próximo passo não
  ficam em uma fila única verificável (`03-Projeto/01-Escopo.md`, §§2–4; `03-Projeto/requisitos.md`, RQ-003).
- **Estado desejado:** o SDR abre uma fila e vê cada lead capturado com origem, imóvel de
  interesse, estado, consentimento, último evento e próximo passo, podendo assumir exceções humanas.
- **Decisões já fechadas:** atendimento consultivo permanece humano; o painel não negocia, não
  classifica high/low sozinho e não apaga histórico; o primeiro incremento precisa ser demonstrável.
- **Bloqueios:** **BLOQUEIO** — confirmar superfície/plataforma do painel, armazenamento, chave do
  lead, integração com conversa e matriz de acesso aos campos pessoais.

## Resultado observável

Após um evento válido de captura, o SDR abre o painel e localiza um cartão único de lead. O cartão
exibe origem, imóvel/código quando houver, estado `Em Atendimento`, referência de conversa,
consentimento, último evento e próximo passo. O SDR pode registrar pendência ou próximo passo sem
perder a origem; uma falha de captura aparece em fila de pendências.

## Limites e dependências

- **Inclui:** fila inicial; cartão de lead; ordenação por entrada/pendência; estado mínimo; próximo
  passo; referência de conversa; leitura e atualização autorizada; auditoria.
- **Fora de escopo:** busca completa de imóveis; agenda; mensagens automáticas; agente autônomo;
  classificação de valor; migração; histórico integral de conversa sem permissão.
- **Entradas e pré-condições:** evento/lead de SPEC-1-001; fonte aprovada; `lead_id`, origem,
  `contact_ref`, `property_code`, estado, consentimento e timestamps.
- **Saídas/artefatos:** fila; cartão; evento de alteração; pendência; log de acesso/alteração.
- **Dependências e responsáveis:** captura — SPEC-1-001/Matheus; operação — SDR; permissões — Janeide/Matheus.
- **Atores e permissões mínimas:** sistema cria; SDR lê dados atribuídos e escreve próximo passo/
  pendência; gestor lê tudo autorizado; corretor não edita o cartão nesta fase.
- **Superfícies/arquivos/configurações afetadas:** painel/fila, modelo de Lead, controle de acesso,
  log de auditoria. Plataforma e arquivos concretos são **BLOQUEIO**.
- **Risco e plano B:** painel indisponível ou dado incompleto; manter fila de pendência e operar
  no canal manual, sem descartar evento.
- **Rollback ou reversão:** ocultar nova fila sem apagar fonte; voltar à consulta manual; preservar
  eventos e alterações já auditadas.

## Dados e integrações

| Origem/destino | Fonte de verdade | Campos/contrato | Autenticação/permissão | Timeout/retry/idempotência | Tratamento de erro |
|---|---|---|---|---|---|
| Captura → cartão | evento/Lead da SPEC-1-001 | `lead_id`, `contact_ref`, `origin`, `property_code`, `status`, `consent_status`, `last_event_at`, `next_step`, `conversation_ref` | SDR/gestor conforme papel; telefone completo somente para papel autorizado | atualização idempotente por `lead_id`; não sobrescrever origem | cartão em pendência e log de rejeição |
| Cartão → auditoria | painel aprovado | `actor_id`, `action`, `field`, `old_value`/`new_value` quando permitido, `occurred_at`, `reason` | leitura do gestor; escrita pelo sistema | evento append-only; retry sem duplicar ação | ação bloqueada e alerta |

| Regra de negócio | Condição | Ação/resultado | Exceção | Fonte |
|---|---|---|---|---|
| RN-1 Uma entrada | lead/evento novo | um cartão por `lead_id` | conflito de chave vira pendência | RQ-001/RQ-008 |
| RN-2 Contexto humano | pergunta/negociação fora do catálogo | SDR assume e registra próximo passo | indisponibilidade do SDR cria escalonamento | RQ-003 |
| RN-3 Origem protegida | cartão existente | origem não pode ser editada pelo SDR | correção exige gestor, motivo e auditoria | D-106; RQ-010 |
| RN-4 Privacidade por papel | leitura/alteração | mostrar somente campos permitidos | permissão negada não revela valor | RQ-010 |
| RN-5 Texto operacional | próximo passo/pendência informado pelo SDR | tratar como texto, escapar apresentação e não executar conteúdo | conteúdo indevido é bloqueado/escalado | RQ-010 |

## Fluxo e regras

1. Sistema recebe lead confirmado da SPEC-1-001.
2. Cria ou atualiza um cartão único, preservando origem e histórico.
3. Fila exibe `Em Atendimento` ou `Pendente de captura`, com ordenação determinística por timestamp.
4. SDR abre o cartão, vê contexto mínimo e registra próximo passo/pendência.
5. Gestor pode revisar auditoria; nenhuma ação dispara mensagem ou agenda nesta SPEC.
6. Falha de acesso, dado incompleto ou conflito fica visível e recuperável.

| Cenário | Dado/condição | Resultado esperado | Caminho de erro/recuperação |
|---|---|---|---|
| Principal | lead válido da captura | cartão único aparece na fila com origem e estado | nenhum |
| Atualização | mesmo `lead_id` com novo evento | cartão atualiza último evento sem perder origem/histórico | divergência vira pendência |
| Consultivo | pergunta fora do padrão | SDR registra próximo passo e mantém contexto | escalonar se SDR indisponível |
| Limite | telefone/nota sem permissão | campo é ocultado e ação bloqueada | log de acesso negado |
| Falha | evento sem `lead_id` ou painel indisponível | pendência correlacionada; nenhum cartão falso | operação manual temporária |

## Instruções de execução para o Ethos

1. **Ler antes de alterar:** `03-Projeto/02-Escopo-Definitivo.md` §§3–6 e Fase 1; `03-Projeto/requisitos.md` RQ-003/RQ-008/RQ-010; SPEC-1-001.
2. **Alterar somente:** fila, cartão, estados mínimos, próximo passo, permissões e auditoria da primeira vertical.
3. **Não alterar:** catálogo completo, agenda, mensagens automáticas, CRM fonte, política high/low ou agente.
4. **Executar nesta ordem:** confirmar modelo de Lead → criar cartão → aplicar papel SDR/gestor → testar atualização → testar acesso/falha → demonstrar.
5. **Parar e pedir validação quando:** campo, fonte, retenção, papel ou armazenamento não estiver confirmado.
6. **Estado válido ao parar:** evento de captura e pendências continuam recuperáveis; operação manual permanece possível.

## Checklist de execução

- [ ] superfície e armazenamento aprovados;
- [ ] modelo de cartão e campos pessoais validados;
- [ ] permissões SDR/gestor testadas;
- [ ] criação, atualização, pendência e auditoria exercitadas;
- [ ] dados de teste não contêm PII real desnecessária;
- [ ] SDR demonstra a fila e confirma o handoff.

## Critérios de aceite

- [ ] **CA-1-05:** cada lead válido da SPEC-1-001 aparece uma vez na fila com origem e estado.
- [ ] **CA-1-06:** SDR registra próximo passo sem alterar origem nem apagar histórico.
- [ ] **CA-1-07:** permissão negada oculta/bloqueia campo e gera log, sem vazar valor.
- [ ] **CA-1-08:** evento incompleto ou painel indisponível cria pendência correlacionada, sem cartão falso.

## TDD da SPEC

| Etapa | Prova | Comando/ação | Resultado esperado | Evidência |
|---|---|---|---|---|
| RED | operação atual | localizar um lead capturado sem cartão unificado | contexto/origem/próximo passo não são recuperáveis em uma tela | captura do estado atual |
| GREEN | cartão novo | usar lead fixture `lead-001` e abrir fila | um cartão mostra origem, código, estado e último evento | captura + ID do cartão |
| GREEN | ação SDR | registrar `next_step=validar necessidade` | próximo passo aparece com ator e horário; origem fica intacta | log de auditoria |
| REFACTOR/REGRESSÃO | permissão, dado incompleto e duplicidade | testar papel corretor, evento sem lead_id e segundo evento | bloqueio/pendência corretos; nenhum vazamento ou cartão duplicado | relatório de cenários |

**Dados/fixtures:** `lead-001` com contato de teste, origem Instagram, código de imóvel e consentimento;
conta/ambiente de teste e armazenamento são **BLOQUEIO**.
**Caminhos de erro obrigatórios:** permissão negada, dado ausente, lead duplicado, painel indisponível,
  origem imutável, texto operacional indevido e PII sem autorização.
**Evidência exigida:** captura da fila/cartão, log de alteração/acesso, pendência e aceite do SDR.

## Handoff e operação

- **Como demonstrar:** abrir um lead criado, localizar cartão, registrar próximo passo e simular erro.
- **Como operar depois:** SDR trata fila e pendências; gestor revisa acesso/auditoria.
- **Como monitorar:** cartões órfãos, pendências antigas, falhas de acesso e divergência de origem.
- **Pendência conhecida:** plataforma, armazenamento, retenção e papéis concretos precisam de validação.

## Tasks vinculadas

| ID | Task | Critério binário | Recorte da prova | Evidência | Status |
|---|---|---|---|---|---|
| F1-T02 | Fechar superfície do painel, modelo Lead e matriz de acesso | plataforma, armazenamento, campos e papéis SDR/gestor aprovados | Contexto; Dados; Checklist | mapa de campos, papéis e ambiente | PENDENTE |
| F1-T06 | Configurar fila e cartão mínimo de lead | lead válido aparece uma vez com origem, estado e contexto | Resultado; Fluxo 1–6; CA-1-05/06 | captura do cartão e auditoria | BLOQUEADA |
| F1-T10 | Exercitar permissões, auditoria e dados incompletos do painel | acesso negado, lead incompleto e painel indisponível são recuperáveis | Cenários; RN-3–RN-5 | log de acesso, pendência e sem vazamento | BLOQUEADA |
| F1-T14 | Demonstrar fila, próximo passo e auditoria do lead | CA-1-05 a CA-1-08 passam sem vazamento | TDD; Handoff | captura, log e aceite SDR | BLOQUEADA |

## Emendas

<!-- Append-only: mudanças aprovadas depois da geração. -->

| Data | Origem do sinal | Micro-spec/task | Motivo |
|---|---|---|---|
| | | | |
