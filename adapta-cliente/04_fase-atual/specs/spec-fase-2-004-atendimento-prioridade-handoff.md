# SPEC-2-004 — Atendimento consultivo, prioridade e próximo passo

**Fase:** 2  
**Status:** bloqueada pelas SPEC-2-002/003 e por B2-08; prioridade produtiva bloqueada por B2-05  
**Dono:** Janeide/gestão + SDR + Champion  
**Origem no escopo:** RQ-003, RQ-008, RQ-010; C2; CI-101; Fase 2  
**Degrau da solução:** construção mínima — organizar contexto, exceção e próximo passo; classificação automática fica bloqueada até regra humana.

## Contexto e decisões fechadas

- **Estado atual:** a Fase 1 possui fila/cartão mínimo e contexto do lead. O escopo definiu atenção prioritária para clientes de maior valor e caminho automatizável para os demais, mas ICP, limiares e regras não foram aprovados.
- **Estado desejado:** o SDR trabalha uma fila com contexto do lead, resultado da busca/card, exceção e próximo passo. Prioridade é manual ou `Não classificada` até B2-05; nenhuma automação inventa high-ticket.
- **Decisões fechadas:** atendimento, negociação e exceções são humanas; perguntas fora do catálogo voltam ao SDR; toda alteração relevante deixa ator/horário/motivo.
- **Bloqueios:** B2-05 para classificação/regras produtivas; B2-04 para PII/histórico; B2-08 para matriz de acesso e contrato humano de handoff; SPEC-2-002/003 aceitas.

## Resultado observável

Um SDR autorizado abre um lead, vê origem, imóvel/contexto, buscas/cards e pendências, registra próximo passo e realiza handoff sem perder histórico. Casos fora do catálogo ficam explicitamente com dono. Enquanto B2-05 estiver aberto, a fila não atribui prioridade automática.

## Limites e dependências

- **Inclui:** contexto agregado; estado de atendimento; prioridade manual/não classificada; motivo; próximo passo; handoff; filtros operacionais e auditoria.
- **Fora:** score IA; classificação autônoma; negociação; distribuição automática; SLA inventado; agenda confirmada; no-show.
- **Entradas:** lead, origem, contexto, eventos de busca/card, decisão humana de prioridade e próximo passo.
- **Saídas:** fila/visão, estado, prioridade, dono, motivo, próximo passo e histórico.
- **Permissões:** a matriz F1 permanece até B2-08. O contrato de handoff deve definir quem transfere, destinatários permitidos e o acesso do dono anterior (padrão recomendado: perde alteração e PII operacional; eventual leitura histórica exige justificativa e regra explícita). Gestor audita; sistema não amplia carteira/papel.
- **Superfícies:** fila/cartão F1, linha do tempo do lead, registro de próximo passo, prioridade humana e recibo de handoff; logs sanitizados.
- **Risco/plano B:** operar por ordem de chegada e prioridade manual enquanto B2-05 estiver aberto; sem B2-08, não habilitar handoff novo.
- **Rollback:** desativar filtros/regras F2 e manter fila F1 com histórico preservado.

## Dados e regras

| Regra | Condição | Resultado | Exceção |
|---|---|---|---|
| RN-231 | B2-05 aberto | `Não classificada` ou prioridade humana com ator/motivo | nenhuma prioridade automática |
| RN-232 | pergunta/imóvel fora do catálogo | pendência atribuída ao SDR com contexto | não encerrar nem sugerir imóvel inventado |
| RN-233 | próximo passo alterado | registrar dono, prazo se informado, ator, horário e motivo | prazo não informado permanece pendente, não é inventado |
| RN-234 | handoff autorizado conforme B2-08 | novo dono aceita/visualiza contexto; dono anterior perde alteração e PII operacional por padrão | falha mantém dono anterior e sinaliza pendência; leitura residual só com regra explícita |
| RN-235 | papel/carteira sem permissão | negar leitura de PII e alteração; registrar tentativa com dados minimizados | gestor audita conforme matriz B2-08 |
| RN-236 | evento de captura, busca, card, prioridade, próximo passo ou handoff repetido | anexar uma vez à linha do tempo por chave de correlação | novo evento consciente recebe nova correlação |

## Fluxo e recuperação

1. Abrir lead na fila autorizada.
2. Exibir origem, contexto, busca/card e pendências correlacionadas.
3. SDR registra atendimento e próximo passo.
4. Se aplicável, registra prioridade manual com motivo; sem regra, mantém `Não classificada`.
5. Caso fora do catálogo recebe pendência/dono.
6. Handoff exige destinatário autorizado e preserva histórico.
7. Falha de handoff ou persistência não altera silenciosamente o dono/estado anterior.

| Cenário | Condição | Resultado | Recuperação |
|---|---|---|---|
| Principal | lead com ficha e próximo passo | contexto e ação persistidos | não aplicável |
| Limite | caso fora do catálogo | pendência SDR, sem recomendação inventada | tratamento humano |
| Falha | handoff/permissão/persistência falha | estado anterior preservado + erro recuperável | repetir com mesma correlação |

## Instruções para o Ethos

1. Ler SPEC-2-002 aceita, contrato de painel F1 e decisão B2-05.
2. Alterar somente fila/contexto/prioridade manual/próximo passo/handoff.
3. Não criar score, IA, limiar, SLA, distribuição, agenda ou negociação.
4. Provar primeiro contexto e próximo passo; depois bordas de prioridade/handoff/permissão.
5. Parar se a implementação exigir escolher regra de ICP/high-ticket ou ampliar papéis.
6. Ao parar, a fila F1 segue funcional e toda prioridade não aprovada permanece desativada.

## Checklist

- [ ] contexto correlacionado demonstrado;
- [ ] próximo passo e dono persistidos;
- [ ] fora do catálogo vira pendência humana;
- [ ] prioridade automática recusada sem B2-05;
- [ ] handoff/permissões e falha exercitados;
- [ ] aceite SDR/gestor registrado.

## Critérios de aceite

- [ ] **CA-2-019:** fila mostra origem, contexto, último evento de catálogo/card, dono e próximo passo sem misturar leads.
- [ ] **CA-2-020:** SDR registra próximo passo e alteração deixa ator, horário e motivo quando aplicável.
- [ ] **CA-2-021:** caso fora do catálogo cria pendência atribuída ao SDR, sem dado/recomendação inventada.
- [ ] **CA-2-022:** com B2-05 aberto, prioridade automática é impossível e o estado fica `Não classificada` ou manual auditável.
- [ ] **CA-2-023:** handoff autorizado por B2-08 preserva histórico, exige confirmação do novo dono e revoga do dono anterior alteração e PII operacional; falha mantém o estado anterior.
- [ ] **CA-2-024:** usuário sem papel/carteira não lê PII nem altera lead indevido; gestor audita a tentativa com dados minimizados.

## TDD da SPEC

| Etapa | Prova | Ação | Resultado | Evidência |
|---|---|---|---|---|
| RED | tentar prioridade automática e handoff sem regra/papel | executar antes da F2 | recusas esperadas | relatório RED |
| GREEN | lead com ficha + caso fora do catálogo | registrar próximo passo, pendência e handoff permitido | CA-2-019..023 passam | snapshots + eventos |
| REGRESSÃO | carteira alheia, falha de persistência e retry | executar bordas | CA-2-024 e preservação do estado passam | log sanitizado |

**Fixtures:** dois SDRs, gestor, leads de carteiras distintas, um imóvel elegível e um caso fora do catálogo.  
**Evidência:** capturas da fila, histórico de eventos, teste de 403/negação, falha/retry e aceite humano.

## Handoff e operação

- **Demonstrar:** abrir fila, tratar lead com ficha, registrar caso fora do catálogo, próximo passo e handoff.
- **Operar:** SDR mantém dono/próximo passo; gestor aprova futuras regras de prioridade.
- **Monitorar:** sem próximo passo, não classificado, pendência sem dono, handoff falho e tentativa negada.
- **Pendência:** B2-05 precisa de decisão humana antes de qualquer prioridade automática.

## Tasks vinculadas

| ID | Task | Dono | SPEC | Critério | Recorte da prova | Evidência esperada | Pré-condições | Status |
|---|---|---|---|---|---|---|---|---|
| F2-T07 | Implementar contexto, próximo passo e pendência fora do catálogo | Ethos | SPEC-2-004 | CA-2-019 a CA-2-021 | GREEN com lead, ficha, próximo passo e caso fora do catálogo | fila, eventos, pendência e histórico | F2-T04 aceita | BLOQUEADA |
| F2-T08 | Provar prioridade conservadora, handoff, carteira e recuperação | Ethos | SPEC-2-004 | CA-2-022 a CA-2-024 | REGRESSÃO com B2-05 aberto, handoff permitido/falho, carteira alheia e retry | capturas, eventos, 403/negação, logs sanitizados e aceite | F2-T07 aceita; regra B2-05 continua bloqueada ou foi aprovada por humano | BLOQUEADA |

## Emendas

| Data | Origem | Micro-spec/task | Motivo |
|---|---|---|---|
