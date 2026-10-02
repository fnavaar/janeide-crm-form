# AP-2026-10-02-2140 — vocabulário de availability diverge entre Fase 1 e catálogo versionado F2

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T05 / SPEC-2-003 (CA-2-013)
- Sinal: hooks novos do card/envio F2 copiaram a checagem da F1 (`availability_status !== 'ativo'`, vocabulário da coleção `properties`), mas a carga versionada da F2 grava `availability_status: 'active'` (vocabulário do export Kenlo mapeado no contrato F2-T01). Resultado: todo item da versão ativa era bloqueado como "indisponível" no card e no envio. A F2-T03 não detectou porque a busca apenas exibe o status, sem validá-lo.
- Evidência: teste humano A2 (Janeide, 2026-10-01) — "Card bloqueado: imóvel indisponível na versão (status: active)"; fixture em `pocketbase/hooks/catalogo_importar.js` grava `availability_status: 'active'` nas 5 linhas; correção em 0.0.96 (`4cdd865`) aceitando `['active','ativo']` nos hooks `card_f2t05.js` e `envio_f2t05.js`; QA 5/5 PASS e A2 aprovado em seguida.
- Regra reutilizável: ao reutilizar lógica de validação de uma fase anterior sobre dados de outra fonte, conferir o vocabulário REAL dos campos na nova fonte (ler a fixture/carga, não o código antigo) antes de copiar a condição; campos de enumeração com mesma semântica podem ter literais diferentes entre coleções.
- Quando aplicar: qualquer hook/validação que leia snapshot_json da carga versionada F2 (card, envio, visitas futuras, indicadores).
- Quando não aplicar: coleções da Fase 1 (`properties`), onde 'ativo' permanece o literal correto.
- Confiança: alta — causa confirmada na fixture e correção validada por teste humano aprovado.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
