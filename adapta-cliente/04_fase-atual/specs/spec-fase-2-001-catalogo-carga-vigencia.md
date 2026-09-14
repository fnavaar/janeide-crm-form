# SPEC-2-001 — Catálogo mínimo, carga e vigência

**Fase:** 2  
**Status:** planejada; execução real bloqueada por B2-01/B2-02/B2-04  
**Dono:** Champion + responsável de cadastro/imóveis  
**Origem no escopo:** RQ-002, RQ-008, RQ-010; C2; Fase 2; D-101  
**Degrau da solução:** dependência existente + construção mínima — manter catálogo mínimo replicado no Skip, sem presumir API do Kenlo.

## Contexto e decisões fechadas

- **Estado atual:** a Fase 1 provou ficha por código e envio humano com fixture/catálogo mínimo. O contrato F1-T03 define Kenlo Mob como fonte operacional e carga por exportação/importação manual; não há API/homologação autorizada.
- **Estado desejado:** uma carga aceita cria uma versão de catálogo consultável, preserva a referência da fonte, identifica pendências e permite reconstruir o resultado da importação.
- **Decisões já fechadas:** os dez campos mínimos são `property_code`, `title`, `availability_status`, `price`, `condominium_fee`, `iptu`, `key_attributes`, `media_urls`, `source_ref`, `valid_until`; não inventar preço/taxa; mídia só da fonte permitida; Kenlo e painel continuam em paralelo.
- **Bloqueios:** B2-01 amostra/layout; B2-02 data de corte/vigência/responsável; B2-03 acesso independente ao Skip; B2-04 política de dado/log.

## Resultado observável

Um operador autorizado submete uma fixture ou lote permitido e recebe um recibo com versão, hash/referência, totais aceitos/recusados e motivos. A versão anterior permanece recuperável; itens sem fonte, vigência ou campos obrigatórios não viram opção ativa.

## Limites e dependências

- **Inclui:** contrato de importação; validação; versão da carga; upsert por `property_code`; lista de pendências; reconciliação e rollback lógico.
- **Fora de escopo:** API/scraping do Kenlo; migração integral; edição do Kenlo; cadastro de proprietário; agenda; classificação de lead.
- **Entradas:** fixture sintética; depois, export autorizado e minimizado.
- **Saídas:** `catalog_import_receipt`, versão de catálogo, dicionário versionado de normalização de bairro/tipo, relatório de recusas e lista de vencidos/pendentes.
- **Atores/permissões:** responsável de cadastro importa/corrige; SDR lê; gestor audita; nenhum lead acessa a carga.
- **Superfícies:** coleção/tabela de catálogo e versões, rota administrativa autenticada ou mecanismo de carga provado, painel de pendências, logs sanitizados.
- **Risco/plano B:** se o mecanismo automático não for provado no ambiente, usar importação administrativa/manual idempotente com o mesmo contrato e recibo.
- **Rollback:** desativar a versão nova e restaurar a anterior por referência; nunca apagar histórico para esconder erro.

## Dados e integrações

| Origem/destino | Fonte de verdade | Contrato | Permissão | Idempotência/erro |
|---|---|---|---|---|
| Export Kenlo → catálogo mínimo | arquivo aprovado, data de corte e `source_ref` | 10 campos mínimos + `import_id` + `catalog_version` | responsável de cadastro | mesma chave+conteúdo não duplica; divergência vira pendência |
| Catálogo → busca/card | versão ativa aceita | somente registros ativos, vigentes e válidos | leitura SDR/gestor | item inválido não é opção ativa |

| Regra | Condição | Resultado | Exceção/fonte |
|---|---|---|---|
| RN-201 | `property_code`, título, status, fonte ou vigência ausente | recusar/pendenciar item | contrato F1-T03 |
| RN-202 | preço não definido pela operação | exibir “consulte”, sem inventar valor | decisão fechada no contrato F1-T03 |
| RN-203 | condomínio/IPTU ausentes | manter ausente e exibir “não informado”, sem preenchimento inventado | decisão F1-T03 |
| RN-204 | URL de mídia fora da allowlist derivada da carga, sem HTTPS ou com redirect para domínio não permitido | bloquear mídia/card ativo; nesta fase é proibido fetch server-side da mídia | RN-5 F1 |
| RN-205 | mesmo hash normalizado do lote, ainda que com novo `import_id` | retornar recibo idempotente, sem nova versão materialmente duplicada | hash do conteúdo normalizado |
| RN-206 | lote parcial ou inválido | não promover silenciosamente; apresentar totais e motivos | gate humano de promoção |
| RN-207 | versão promovida é substituída/rollback | derivados históricos preservam `catalog_version` e exibem “versão substituída”; novo envio exige versão ativa | rollback não destrutivo |

## Fluxo e recuperação

1. Validar autorização, formato, data de corte e referência da fonte.
2. Rodar validação sem promover dados.
3. Mostrar aceitos, recusados, alterações e pendências.
4. O operador autorizado confirma a promoção da versão.
5. Registrar recibo e preservar versão anterior.
6. Em falha, manter versão anterior ativa e disponibilizar correção/reprocessamento idempotente.

| Cenário | Condição | Resultado | Recuperação |
|---|---|---|---|
| Principal | lote válido autorizado | versão promovida e recibo reconciliável | não aplicável |
| Limite | campo opcional ausente | item preservado sem valor inventado | correção posterior versionada |
| Falha | obrigatório ausente, mídia insegura ou lote interrompido | recusa/pendência; versão anterior ativa | corrigir e reprocessar com mesma correlação |

## Instruções para o Ethos

1. Ler o contrato de catálogo F1-T03 e esta SPEC.
2. Alterar somente o modelo/carga/versionamento e superfícies de pendência necessárias.
3. Não criar integração Kenlo, agenda, classificação de lead ou envio automático.
4. Executar fixture → validação → recibo → promoção controlada → rollback lógico.
5. Parar se B2-01/B2-02/B2-04 impedirem dado real ou se o ambiente não permitir prova segura.
6. Ao parar, manter a Fase 1 funcional e nenhum lote parcial promovido.

## Checklist

- [ ] contrato da carga e campos validados;
- [ ] fixture sintética exercitada;
- [ ] idempotência e lote parcial testados;
- [ ] lista de pendências/vencidos demonstrada;
- [ ] recibo e rollback lógico anexados;
- [ ] aceite do Champion e responsável de cadastro registrado.

## Critérios de aceite

- [ ] **CA-2-001:** lote válido produz recibo com `import_id`, versão, fonte, data de corte e totais.
- [ ] **CA-2-002:** registro ativo/vigente preserva os campos da fonte sem inventar ausências.
- [ ] **CA-2-003:** obrigatório ausente, vigência inválida ou mídia insegura não vira opção ativa e aparece com motivo.
- [ ] **CA-2-004:** repetir o mesmo lote não cria segunda versão materialmente duplicada nem duplica imóveis.
- [ ] **CA-2-005:** falha parcial mantém a versão anterior ativa e permite reprocessamento rastreável.
- [ ] **CA-2-006:** somente papel autorizado promove/corrige versão; SDR permanece somente leitura.

## TDD da SPEC

| Etapa | Prova | Ação | Resultado | Evidência |
|---|---|---|---|---|
| RED | fixture com válido, ausente, vencido e URL insegura | validar antes da implementação | contrato ainda não separa todos os resultados | relatório RED |
| GREEN | fixture mínima | importar/promover/repetir | CA-2-001..004 passam | recibos e snapshot da lista |
| REGRESSÃO | falha parcial + acesso SDR | interromper lote e tentar promover como SDR | versão anterior preservada e 403/negação | log sanitizado + recibo |

**Fixtures:** somente dados sintéticos até B2-01/B2-02/B2-04.  
**Evidência exigida:** fixture, recibo, diff da versão, relatório de pendências, prova de idempotência, autorização e aceite humano.

## Handoff e operação

- **Demonstrar:** validar lote, revisar diferenças, promover e abrir pendências.
- **Operar:** responsável de cadastro mantém versão/vigência; SDR consome versão ativa.
- **Monitorar:** itens vencidos, recusas, carga parcial e divergência entre fonte/painel.
- **Pendência:** mecanismo real e conta autorizadora dependem de B2-01/B2-03.

## Tasks vinculadas

| ID | Task | Dono | SPEC | Critério | Recorte da prova | Evidência esperada | Pré-condições | Status |
|---|---|---|---|---|---|---|---|---|
| F2-T01 | Fechar contrato da carga, fonte, vigência e política do catálogo | Champion | SPEC-2-001 | CA-2-001 a CA-2-003 | validar fixture e registrar B2-01/B2-02/B2-04 ou decisões fechadas | contrato da carga, fixture, relatório de validação e aceite | autorização explícita; sem dado real | ELEGÍVEL |
| F2-T02 | Implementar carga versionada, idempotência e rollback lógico | Ethos | SPEC-2-001 | CA-2-004 a CA-2-006 | GREEN/REGRESSÃO com repetição, falha parcial e permissão | recibos, diff de versão, 403/negação e rollback | F2-T01 aceita; B2-03 resolvido por acesso ou prova exportável | BLOQUEADA |

## Emendas

| Data | Origem | Micro-spec/task | Motivo |
|---|---|---|---|
