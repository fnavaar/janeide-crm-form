# SPEC-2-002 — Busca consultiva e ficha vigente

**Fase:** 2  
**Status:** bloqueada pela aceitação da SPEC-2-001  
**Dono:** Champion + SDR  
**Origem:** RQ-002/RQ-003/RQ-008/RQ-010; C2; Fase 2  
**Degrau:** construção mínima — ampliar a consulta por código da F1 para busca controlada por código, bairro e tipo sobre catálogo versionado.

## Contexto e decisões fechadas

- **Atual:** F1 consulta ficha por código e bloqueia item inválido; o SDR ainda não possui busca consultiva consolidada.
- **Desejado:** busca reproduzível por código, bairro e tipo, com filtros combináveis, estado vazio honesto e ficha vinculada à versão da fonte.
- **Fechado:** catálogo mínimo replicado; leitura pelo SDR; `consulte` é distinto de ausente/erro; item vencido/inativo não aparece como opção ativa; sem API Kenlo presumida.
- **Bloqueios:** versão aceita da SPEC-2-001; B2-03 para prova independente; definição controlada dos valores de bairro/tipo na carga.

## Resultado observável

O SDR pesquisa uma amostra aprovada por código, bairro ou tipo e recebe resultados vigentes com fonte/versão. Zero resultado, dado incompleto e divergência são estados visíveis; nenhum dado é preenchido por inferência.

## Limites e dependências

- **Inclui:** busca, filtros, ordenação determinística, ficha completa da amostra, estado vazio, paginação/limite e vínculo com versão.
- **Fora:** recomendação por IA, ranking comercial automático, geolocalização inferida, agenda, alteração do catálogo pela busca.
- **Entradas:** catálogo ativo aceito; vocabulário de bairro/tipo proveniente da fonte.
- **Saídas:** lista e ficha com `source_ref`, `catalog_version`, vigência e estado.
- **Permissões:** SDR/gestor leem; responsável de cadastro corrige na superfície própria; lead não acessa painel interno.
- **Superfícies:** busca/filtros e ficha de leitura no painel F1; coleção versionada de catálogo somente por leitura; estado vazio/pendência; logs sanitizados.
- **Risco/plano B:** busca textual pode produzir falso positivo; fallback é filtro exato/normalizado e consulta por código.
- **Rollback:** desligar filtros novos e manter consulta por código da F1.

## Dados e regras

| Regra | Condição | Resultado | Exceção |
|---|---|---|---|
| RN-211 | código exato existente e ativo | uma ficha da versão ativa | duplicidade de código bloqueia resultado |
| RN-212 | bairro/tipo normalizado | somente itens correspondentes | valor desconhecido retorna vazio, não aproximação silenciosa |
| RN-213 | `price` explicitamente “consulte” | mostrar “Consulte” | nulo por erro vira pendência, não “Consulte” |
| RN-214 | item vencido/inativo/incompleto | não listar como opção ativa; motivo auditável | gestor pode consultar pendências, não oferecê-las |
| RN-215 | mídia fora da allowlist | omitir/bloquear mídia e card | nunca buscar URL arbitrária no cliente |
| RN-216 | consultas repetidas | mesmo conjunto para mesma versão/filtros | mudança exige nova versão identificável |

## Fluxo e recuperação

1. Validar papel e versão ativa.
2. Normalizar apenas segundo dicionário da carga.
3. Consultar por código ou filtros combinados.
4. Exibir resultados com fonte, vigência e pendências.
5. Abrir ficha sem alterar catálogo.
6. Em indisponibilidade, mostrar falha recuperável e manter consulta por código/fallback manual.

## Instruções para o Ethos

1. Ler SPEC-2-001 e contratos F1 de catálogo/painel.
2. Alterar apenas busca, leitura e ficha.
3. Não criar API Kenlo, agenda, classificação, envio automático ou campos sem fonte.
4. Implementar código → bairro → tipo → combinação → vazio → inválido → permissão.
5. Parar se a versão ativa ou o vocabulário não estiverem aprovados.
6. Preservar a consulta F1 ao parar.

## Checklist

- [ ] filtros e normalização documentados;
- [ ] principal/vazio/inválido exercitados;
- [ ] `consulte` distinto de ausência;
- [ ] mídia e permissão testadas;
- [ ] vínculo à versão demonstrado;
- [ ] SDR aprovou o roteiro.

## Critérios de aceite

- [ ] **CA-2-007:** código exato ativo retorna uma ficha identificando fonte, versão e vigência.
- [ ] **CA-2-008:** bairro e tipo, isolados ou combinados, retornam somente itens correspondentes da versão ativa.
- [ ] **CA-2-009:** resultado vazio é apresentado como vazio, sem imóvel ou valor inventado.
- [ ] **CA-2-010:** `consulte`, ausente, vencido, inativo e divergente são estados distintos e observáveis.
- [ ] **CA-2-011:** URL fora da allowlist e item inválido não são oferecidos como ficha ativa.
- [ ] **CA-2-012:** ator sem papel autorizado não acessa ficha interna nem PII do lead por esta superfície.

## TDD da SPEC

| Etapa | Prova | Ação | Esperado | Evidência |
|---|---|---|---|---|
| RED | fixture com bairros/tipos e estados mistos | executar filtros atuais | busca completa ainda não existe | relatório RED |
| GREEN | códigos e filtros aprovados | executar 6 consultas | CA-2-007..010 passam | matriz consulta→resultado |
| REGRESSÃO | URL insegura + usuário sem papel + versão trocada | consultar | bloqueio/negação e versão explícita | log sanitizado + capturas |

**Fixtures:** catálogo sintético versionado com ativo, consulte, ausente, vencido e inativo.  
**Evidência:** matriz de consultas, capturas, IDs/versão, prova 403/negação e aceite SDR.

## Handoff e operação

- **Demonstrar:** buscar por três chaves, abrir ficha e mostrar estados vazio/bloqueado.
- **Operar:** SDR pesquisa; cadastro corrige a fonte/carga; gestor audita.
- **Monitorar:** zero resultados, filtros sem vocabulário, itens vencidos e URLs bloqueadas.

## Tasks vinculadas

| ID | Task | Dono | SPEC | Critério | Recorte da prova | Evidência esperada | Pré-condições | Status |
|---|---|---|---|---|---|---|---|---|
| F2-T03 | Implementar busca por código, bairro e tipo sobre versão ativa | Ethos | SPEC-2-002 | CA-2-007 a CA-2-009 | GREEN com tabela esperado×obtido da fixture versionada | resultados, fichas, source_ref e vigência | F2-T02 aceita; contrato de normalização derivado da amostra | BLOQUEADA |
| F2-T04 | Provar bloqueios, estados vazios, indisponibilidade e permissão da busca | Ethos | SPEC-2-002 | CA-2-010 a CA-2-012 | REGRESSÃO com inativo, vencido, incompleto, zero, indisponível e acesso negado | relatório de cenários, capturas e logs sanitizados | F2-T03 aceita | BLOQUEADA |

## Emendas

| Data | Origem | Micro-spec/task | Motivo |
|---|---|---|---|
