# AP-2026-10-02-2141 — roteiro humano deve citar códigos da versão ativa, não de fases anteriores

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T05 / SPEC-2-003
- Sinal: roteiro de teste humano da F2-T05 usou `CASAS-TURIM-001` (código da coleção `properties` da Fase 1) como imóvel principal; o card F2 deriva da versão ativa do catálogo (`catalog_version_items`), onde os códigos reais são `F2-T01-001`/`F2-T01-002`. A validadora recebeu bloqueio `not_in_active_version` correto do sistema e parou para confirmar — comportamento correto do produto, roteiro errado.
- Evidência: relato de Janeide (2026-10-01, A2); logs do Skip 55154 confirmam GET card 404→409→200 conforme correções; roteiro corrigido em `artifacts/f2-t05-roteiro-teste-humano.md` com F2-T01-002 (card completo), F2-T01-001 (bloqueio RN-3 por price null) e CASAS-TURIM-001 realocado como caso positivo de bloqueio (A4).
- Regra reutilizável: roteiro de teste humano de uma fase deve usar SOMENTE identificadores da fonte de dados daquela fase (versão ativa do catálogo na F2), nunca herdados de fases anteriores; quando um código antigo for útil como caso de bloqueio, marcá-lo explicitamente como "fora da fonte — bloqueio esperado".
- Quando aplicar: qualquer roteiro que teste superfícies sobre a fonte versionada F2 (card, envio, visitas, handoff).
- Quando não aplicar: testes de regressão que propositalmente exercitam dados da fase anterior (nesse caso, rotular a expectativa).
- Confiança: alta — bloqueio reproduzido e confirmado como comportamento correto após verificação da fixture.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
