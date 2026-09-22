# Relatório de validação — F2-T01

> Execução local determinística sobre fixture sintética; nenhuma chamada ao Kenlo ou ao Skip foi feita.

## Escopo e baseline

- Fixture: `adapta-cliente/04_fase-atual/fixtures/catalogo-f2-t01.json`.
- Entrada contratual: `.xls`, 29 colunas, fonte Kenlo Mob, corte em `2026-09-15`.
- A fixture é sintética e não contém PII real, credenciais ou dado de imóvel real.
- O baseline do HEAD não continha contrato/fixture/validador da F2-T01; esta execução cria a primeira prova reproduzível.
- `promotion_status` é `validation_only`: não houve promoção de versão nem alteração de catálogo.

## Resultado do recibo

- `import_id`: `import-f2-t01-synthetic-001`.
- `catalog_version`: `cat-20260915-fac83f9cf10a`.
- `content_hash`: `fac83f9cf10a55b9410066fd0061b28b36651131a7569f9ea67ebef6dd18c3cd`.
- Fonte/corte: `Kenlo Mob` / `2026-09-15`.
- Totais: **5** linhas · **2** aceitas · **1** pendentes · **2** recusadas.
- Idempotência contratual: repetir o mesmo conteúdo canônico mantém `content_hash` e `catalog_version`; não cria versão materialmente duplicada.

## Casos exercitados

| Caso | Classificação | Ativo? | Evidência |
|---|---|---:|---|
| `valid_zero_values_no_media` | `accepted` | sim | media_pending_manual_registration |
| `stale_review_but_accepted` | `accepted` | sim | media_pending_manual_registration; stale_review |
| `missing_required_property_code` | `rejected` | não | required_missing:property_code; media_pending_manual_registration |
| `expired_valid_until` | `rejected` | não | invalid_or_expired_valid_until; media_pending_manual_registration |
| `unsafe_manual_media_pending` | `pending` | não | unsafe_media_blocked |

## Critérios F2-T01

| Critério | Resultado | Prova |
|---|---|---|
| CA-2-001 | PASS nesta fixture | Recibo com `import_id`, versão, fonte, data de corte, hash e totais. |
| CA-2-002 | PASS nesta fixture | Linhas aceitas preservam os campos canônicos; zeros monetários viram ausência; mídia ausente vira pendência manual; nenhum valor é inventado. |
| CA-2-003 | PASS nesta fixture | Obrigatório ausente e vigência vencida são recusados; mídia insegura fica pendente e não ativa; motivos aparecem por linha. |

## Checagens executadas

- PASS — zero monetário normalizado para ausência.
- PASS — mídia ausente classificada como pendência manual sem recusar o item.
- PASS — desatualizado aceito com stale_review.
- PASS — obrigatório ausente recusado com motivo.
- PASS — vigência vencida recusada com motivo.
- PASS — mídia insegura pendenciada e nunca ativa.
- PASS — Promotor(es) e Indicador(es) ausentes do catálogo normalizado.
- PASS — hash canônico reproduzido duas vezes sem divergência.

## Limites e próximo gate

- O contrato formaliza versionamento, idempotência, recibo append-only e rollback lógico, mas a implementação executável desses comportamentos não foi iniciada nesta task.
- O parser de `.xls` real, a promoção controlada, o acesso por papel e a prova de rollback pertencem à F2-T02.
- A lista completa das 29 colunas ainda depende da primeira exportação real; os cabeçalhos não confirmados não foram inventados nem copiados para o catálogo mínimo.
- A Fase 1 permanece inalterada.

## Comando reproduzível

```sh
python3 adapta-cliente/04_fase-atual/scripts/validar-f2-t01.py \
  --fixture adapta-cliente/04_fase-atual/fixtures/catalogo-f2-t01.json \
  --receipt adapta-cliente/06_notas/fase-2/recibo-f2-t01.json \
  --report adapta-cliente/06_notas/fase-2/relatorio-f2-t01.md
```
