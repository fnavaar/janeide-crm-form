# SPEC-1-003 — consulta e envio de ficha validada de imóvel

**Fase:** 1  
**Status:** bloqueada  
**Dono:** SDR, com validação de catálogo por Janeide/Matheus  
**Origem no escopo:** C2 inicial, RQ-002, RQ-008, D-101, D-102, AC-101/AC-106  
**Degrau da soluão:** construção mínima — consulta por código e card de uma fonte aprovada, sem sincronização completa ou busca avançada da Fase 2.

## Contexto e decisões fechadas

- **Estado atual:** o atendente alterna site, Kenlo Mob/CRM e WhatsApp para localizar e enviar
  links/fichas (`03-Projeto/01-Escopo.md`, §§2–4; `Analise - IMG_0173.md`).
- **Estado desejado:** a partir de um `property_code` válido, o SDR visualiza uma ficha mínima
  proveniente da fonte vigente, confirma o envio e o vincula ao lead.
- **Decisões já fechadas:** não enviar imóvel indisponível/incompleto; não inventar preço, taxa,
  entrega ou decorado; Fase 1 usa consulta por código; busca por bairro/tipo e catálogo completo
  ficam para Fase 2; envio é iniciado pelo SDR, não por agente.
- **Bloqueios:** **BLOQUEIO** — reconciliar Kenlo Mob/site como fonte de verdade, acesso de
  leitura, campos oficiais, vigência e mecanismo de mídia/WhatsApp.

## Resultado observável

Com um lead na fila e um código de imóvel válido, o SDR abre uma ficha mínima com código, título,
status, preço/taxas quando confirmados, características essenciais, mídia/link e referência da
fonte. O SDR confirma o envio; o sistema registra lead, imóvel, usuário e horário. Dado vencido,
incompleto ou indisponível é bloqueado e explica o motivo.

## Limites e dependências

- **Inclui:** consulta por código; leitura de ficha mínima; validação de status/vigência; preview;
  envio manual confirmado pelo SDR; vínculo ao lead; log.
- **Fora de escopo:** busca por bairro/tipo; sincronização completa; cadastro massivo; atualização
  de preço; recomendação IA; agente autônomo; negociação; agenda.
- **Entradas e pré-condições:** `lead_id`, `property_code`, fonte autorizada, status e `valid_until`
  quando existirem, links de mídia e permissão de leitura.
- **Saídas/artefatos:** preview; mensagem/card enviado; vínculo lead–imóvel; log de fonte/versão;
  bloqueio explicável.
- **Dependências e responsáveis:** fonte/catálogo — Matheus/Janeide; operação — SDR; conteúdo e
  validade — responsável de imóveis a confirmar.
- **Atores e permissões mínimas:** SDR lê e confirma envio; gestor revisa; sistema não edita o
  catálogo nesta SPEC; corretor não altera fonte.
- **Superfícies/arquivos/configurações afetadas:** painel/card, adaptador de catálogo, registro de
  envio e auditoria. Plataforma concreta e mapa de campos são **BLOQUEIO**.
- **Risco e plano B:** fonte indisponível ou divergente; SDR continua manual e registra erro, sem
  enviar dados não confirmados.
- **Rollback ou reversão:** desabilitar preview/envio novo; manter histórico já enviado e voltar ao
  procedimento manual aprovado.

## Dados e integrações

| Origem/destino | Fonte de verdade | Campos/contrato | Autenticação/permissão | Timeout/retry/idempotência | Tratamento de erro |
|---|---|---|---|---|---|
| Painel → catálogo | Kenlo/site ou fonte aprovada | `property_code`, `title`, `availability_status`, `price`, `condominium_fee`, `iptu`, `key_attributes`, `media_urls`, `source_ref`, `valid_until` | leitura aprovada; sem escrita | consulta não duplica; timeout a confirmar; não usar cache vencido | mostrar indisponibilidade/fonte não validada |
| Preview → WhatsApp | conversa autorizada | `lead_id`, `property_code`, `card_version`, `sent_by`, `sent_at`, `message_ref` | SDR confirma; template/conteúdo aprovado | uma ação por confirmação; retry somente com `message_ref` | manter preview e criar pendência, sem envio duplicado |

| Regra de negócio | Condição | Ação/resultado | Exceção | Fonte |
|---|---|---|---|---|
| RN-1 Fonte vigente | ficha consultada | exibir `source_ref` e vigência | sem vigência confirmada, bloquear automatização | RQ-002; D-106 |
| RN-2 Disponibilidade | status ativo confirmado | permitir preview | status ausente/inativo bloqueia | RQ-002 |
| RN-3 Dados comerciais | preço/taxa/entrega presentes e vigentes | exibir exatamente o valor da fonte | ausente/divergente, marcar pendência | escopo definitivo §6 |
| RN-4 Envio humano | SDR clica confirmar | enviar uma vez e registrar | sem confirmação, não enviar | D-102; RQ-003 |
| RN-5 Mídia segura | URL vem da fonte aprovada | exibir somente mídia permitida e tratar URL como dado | URL arbitrária/insegura bloqueia o card | RQ-010; AC-101 |

## Fluxo e regras

1. SDR abre um lead e informa `property_code`.
2. Sistema consulta a fonte aprovada e verifica status/vigência.
3. Sistema monta preview sem preencher campos ausentes e valida links de mídia da fonte aprovada.
4. SDR revisa e confirma o envio; o cliente recebe o card pela conversa autorizada.
5. Sistema registra vínculo, versão da ficha, usuário, horário e referência de mensagem.
6. Falha, dado incompleto ou fonte divergente bloqueia envio e cria pendência.

| Cenário | Dado/condição | Resultado esperado | Caminho de erro/recuperação |
|---|---|---|---|
| Principal | código ativo e ficha vigente | preview correto e envio único confirmado pelo SDR | nenhum |
| Indisponível | status inativo ou ausente | não permitir envio como opção ativa | SDR registra alternativa manual |
| Incompleto | preço/taxa/link obrigatório ausente | exibir bloqueio com campo faltante | responsável atualiza fonte |
| Divergente | fonte retorna versão diferente | exigir reconciliação; não sobrescrever histórico | pendência com `source_ref` |
| Falha | catálogo/WhatsApp indisponível | nenhum sucesso falso; pendência correlacionada | SDR segue manualmente |

## Instruções de execução para o Ethos

1. **Ler antes de alterar:** `03-Projeto/02-Escopo-Definitivo.md` §§3–6 e Fase 1–2; `03-Projeto/requisitos.md` RQ-002/RQ-008; `03-Projeto/03-Setup-Ethos/sugestoes-conectores-automacoes.md`.
2. **Alterar somente:** consulta por código, preview, confirmação humana, vínculo e log da primeira vertical.
3. **Não alterar:** catálogo completo, busca avançada, preço, fonte, migração, recomendação IA ou agenda.
4. **Executar nesta ordem:** validar fonte/campos → consultar código → testar bloqueio → testar preview → confirmar envio → verificar log.
5. **Parar e pedir validação quando:** fonte, status, vigência, preço/taxa, permissão ou template não estiver aprovado.
6. **Estado válido ao parar:** nenhum dado não confirmado foi enviado; preview/manual continua possível.

## Checklist de execução

- [ ] fonte e campos mínimos aprovados;
- [ ] vigência/status e bloqueio de dado incompleto definidos;
- [ ] permissão de leitura e envio do SDR testada;
- [ ] preview, envio único, fonte indisponível e imóvel inativo exercitados;
- [ ] vínculo e log anexados;
- [ ] responsável pela atualização do catálogo confirmado.

## Critérios de aceite

- [ ] **CA-1-09:** código ativo retorna ficha mínima com fonte e vigência identificáveis.
- [ ] **CA-1-10:** SDR confirma um envio e o sistema registra lead, imóvel, versão, usuário e horário.
- [ ] **CA-1-11:** dado incompleto, vencido ou indisponível bloqueia envio como opção ativa.
- [ ] **CA-1-12:** consulta ou retry não gera envio duplicado.

## TDD da SPEC

| Etapa | Prova | Comando/ação | Resultado esperado | Evidência |
|---|---|---|---|---|
| RED | processo atual | pedir uma ficha usando apenas o painel atual | SDR precisa alternar fontes e não há vínculo auditável | captura do processo |
| GREEN | fixture de imóvel ativo | consultar `property_code=CASAS-TURIM-001` no ambiente aprovado | preview mostra campos válidos e fonte | captura + `source_ref` |
| GREEN | confirmação SDR | confirmar envio ao lead `lead-001` | uma mensagem/card e vínculo registrados | `message_ref` + log |
| REFACTOR/REGRESSÃO | inativo, incompleto, timeout e repetição | executar quatro cenários | bloqueios corretos, sem dado inventado ou duplicidade | relatório de cenários |

**Dados/fixtures:** imóvel e lead de teste sem PII real desnecessária; fonte, ambiente e IDs concretos
são **BLOQUEIO**.
**Caminhos de erro obrigatórios:** status inválido, vigência ausente, campo incompleto, timeout,
  permissão negada, retry, fonte divergente e URL de mídia não permitida.
**Evidência exigida:** preview, card enviado, vínculo, fonte/versão, logs e aceite do SDR.

## Handoff e operação

- **Como demonstrar:** informar código, revisar preview, confirmar envio e abrir o vínculo no lead.
- **Como operar depois:** SDR consulta/valida; responsável de catálogo corrige fonte; gestor audita.
- **Como monitorar:** cards bloqueados, dados vencidos, falhas de consulta e envios repetidos.
- **Pendência conhecida:** fonte de verdade, permissão, campos e vigência ainda não confirmados.


## Tasks vinculadas

| ID | Task | Critério binário | Recorte da prova | Evidência | Status |
|---|---|---|---|---|---|
| F1-T03 | Fechar fonte do catálogo, campos, vigência e mídia | fonte única, status, validade, campos e mídia aprovados | Contexto; Dados; Regras RN-1–RN-5 | contrato de catálogo e imóvel de teste | PENDENTE |
| F1-T07 | Configurar consulta por código e preview de ficha | código ativo retorna preview com fonte/vigência sem preencher ausências | Resultado; Fluxo 1–3; CA-1-09/11 | preview, `source_ref` e bloqueio | BLOQUEADA |
| F1-T11 | Exercitar bloqueios de catálogo, mídia e envio duplicado | inativo, incompleto, divergente, URL insegura e retry bloqueiam corretamente | Cenários; RN-1–RN-5 | relatório e logs de bloqueio | BLOQUEADA |
| F1-T15 | Demonstrar ficha vigente e envio humano rastreável | CA-1-09 a CA-1-12 passam sem dado inventado/duplicidade | TDD; Handoff | preview, `message_ref`, vínculo e aceite | BLOQUEADA |

## Emendas

<!-- Append-only: mudanças aprovadas depoiss da gerão. -->

| Data | Origem do sinal | Micro-spec/task | Motivo |
|---|---|---|---|
| | | | |