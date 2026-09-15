# Contrato de carga do catálogo — F2-T01

**Task:** F2-T01 — Fechar contrato da carga, fonte, vigência e política do catálogo  
**SPEC:** SPEC-2-001 — Catálogo mínimo, carga e vigência  
**Versão do contrato:** 1.0  
**Estado:** formalizado para aceite humano; a implementação do mecanismo de carga pertence à F2-T02  
**Data das decisões:** 2026-09-15  
**Responsável pela exportação e pela carga:** Matheus Silva  
**Fonte operacional:** Kenlo Mob  
**Destino:** catálogo mínimo replicado no painel Skip, em paralelo ao Kenlo  

> Este contrato não autoriza API, scraping ou edição do Kenlo, não promove dados reais e não altera
> o catálogo existente. A F2-T01 fecha o formato, a normalização e as regras de validação; a F2-T02
> implementará a carga versionada, a idempotência, as permissões e o rollback no ambiente autorizado.

## 1. Decisões fechadas

### B2-01 — Formato da exportação Kenlo

- A entrada operacional é uma exportação manual do Kenlo em arquivo **`.xls` com 29 colunas**.
- A data de corte é a data em que o arquivo foi exportado. Exemplo: arquivo exportado em
  15/09/2026 tem `cutoff_date = 2026-09-15`.
- Os valores monetários dos campos `R$ Locação`, `R$ Cond.` e `R$ Iptu` iguais a `0` — em
  qualquer representação equivalente do arquivo — significam **não preenchido**. A normalização
  grava ausência (`null`) e a apresentação usa `consulte` para preço ou `não informado` para
  condomínio/IPTU. Zero não pode ser tratado como preço ou taxa real.
- A exportação não contém mídia. A carga inicial grava `media_urls: []` e
  `media_status: pending_manual_registration`. Isso é uma pendência operacional de cadastro,
  **não um erro de validação do lote**.
- A mídia cadastrada depois no Skip fica sujeita à allowlist e às regras de HTTPS da SPEC-2-001;
  URL insegura não pode tornar o imóvel uma opção ativa de card.
- O contrato mapeia somente os campos canônicos e os cabeçalhos explicitamente conhecidos. Os
  demais cabeçalhos das 29 colunas não são adivinhados nem copiados para o catálogo mínimo. A
  primeira exportação real deve fornecer o dicionário de cabeçalhos restante antes da F2-T02.

### B2-02 — Corte, vigência, atualização e responsável

- `cutoff_date` é obrigatório e deve ser igual à data de exportação informada para o arquivo.
  A carga não usa a data de execução como substituta silenciosa.
- A frequência operacional é **semanal**. Frequência não prorroga automaticamente a vigência de
  nenhum imóvel.
- Matheus Silva é responsável pela exportação e pela submissão da carga. O papel autorizado a
  corrigir ou promover uma versão é o responsável de cadastro/imóveis definido para a operação;
  neste ciclo, a decisão operacional foi registrada por Matheus.
- A data `last_updated_at` da fonte é usada apenas para sinalização de desatualização. Um imóvel
  fica `stale_review` quando sua data de atualização é **anterior a mais de seis meses** em
  relação ao `cutoff_date`; exatamente seis meses não é marcado como desatualizado.
- Imóvel `stale_review` entra no catálogo se os demais critérios duros forem válidos. A flag e a
  lista de revisão são mantidas para revisão periódica de permanência, processo separado da
  carga e fora do escopo de recusa automática.
- `valid_until` continua obrigatório para a vigência do registro. A frequência semanal e
  `last_updated_at` não inventam `valid_until`; se a vigência não puder ser validada, o item não
  pode ser opção ativa e aparece como pendência/recusa com motivo.

### B2-04 — Retenção, log e dados operacionais

- Dados da carga — arquivo recebido, snapshot normalizado, recibo e relatório de pendências — têm
  retenção de **1 ano contado da data da carga**. A rotina de expurgo deve respeitar esse prazo e
  não pode apagar o histórico antes dele.
- O log de importação é **append-only por lote**. Cada recibo preserva `import_id`,
  `catalog_version`, `source_ref`, `cutoff_date`, hash do conteúdo normalizado, responsável,
  horário da carga e totais aceitos/pendentes/recusados.
- Lotes anteriores não são sobrescritos. O catálogo ativo aponta para a versão vigente mais
  recente aceita; recibos e versões anteriores continuam acessíveis durante a retenção.
- Rollback é lógico e não destrutivo: desativa a versão apontada como ativa, registra motivo,
  ator e horário, e aponta para uma versão anterior preservada. Nenhum histórico é apagado para
  esconder erro.
- `Promotor(es)` e `Indicador(es)` ficam fora do catálogo mínimo, do snapshot normalizado e dos
  logs operacionais. Não são transformados em campos derivados.
- `Captador(es)` entra somente como `captador_internal`, campo operacional interno para
  rastreabilidade da SPEC-2-003. Não é exibido no card do cliente nem tratado como dado de
  terceiro; o acesso deve seguir a permissão operacional do painel.

## 2. Modelo canônico da carga

A carga normalizada contém os dez campos mínimos da SPEC e metadados do lote. A ausência de um
campo opcional permanece ausência; nenhum valor é preenchido por inferência.

| Campo canônico | Origem/regra | Obrigatoriedade e resultado |
|---|---|---|
| `property_code` | código do imóvel no export | obrigatório; ausente → pendência/recusa, nunca opção ativa |
| `title` | título/nome do imóvel no export | obrigatório; ausente → pendência/recusa |
| `availability_status` | status do imóvel no export | obrigatório; somente status ativo confirmado pode ser candidato |
| `price` | `R$ Locação`; `0` → `null` | opcional quando não definido; ausência aparece como `consulte` |
| `condominium_fee` | `R$ Cond.`; `0` → `null` | opcional; ausência aparece como `não informado` |
| `iptu` | `R$ Iptu`; `0` → `null` | opcional; ausência aparece como `não informado` |
| `key_attributes` | atributos presentes na fonte, sem completar ausências | preservar somente o que veio da fonte |
| `media_urls` | não vem no `.xls`; inicia como `[]` | pendência de cadastro manual, não erro do lote |
| `source_ref` | referência do arquivo + linha; o `content_hash` do lote fica nos metadados e no recibo | obrigatório e rastreável |
| `valid_until` | vigência validada para o item/lote | obrigatório; ausente, inválida ou vencida → não ativo |

Metadados operacionais mínimos:

```json
{
  "import_id": "identificador único da tentativa",
  "catalog_version": "versão derivada do cutoff_date e do hash normalizado",
  "source_ref": "arquivo e linha da fonte",
  "cutoff_date": "YYYY-MM-DD",
  "exported_by": "ator responsável pela exportação",
  "loaded_by": "ator que submeteu a carga",
  "loaded_at": "RFC3339",
  "retention_expires_at": "loaded_at + 1 ano",
  "content_hash": "SHA-256 do conteúdo canônico, sem import_id e loaded_at"
}
```

O valor real de `import_id` e os hashes de produção só surgem na execução autorizada da carga.
A fixture desta task usa identificadores sintéticos explícitos.

## 3. Normalização e validação

### 3.1 Entrada do lote

1. Confirmar extensão `.xls`, contagem declarada de 29 colunas, fonte Kenlo e `cutoff_date`.
2. Confirmar que `cutoff_date` corresponde à data da exportação e que o responsável está
   identificado.
3. Normalizar valores monetários; nunca converter `0` em valor real.
4. Gerar `source_ref` por arquivo/linha e calcular hash do conteúdo normalizado.
5. Validar registros sem promover a versão.

### 3.2 Regras duras

Um item não pode ser candidato ativo quando:

- faltar `property_code`, `title`, `availability_status`, `source_ref` ou `valid_until`;
- `valid_until` for inválido ou anterior ao `cutoff_date`;
- `availability_status` não representar disponibilidade ativa confirmada;
- uma URL de mídia manual informada for insegura, não HTTPS ou fora da allowlist permitida.

O resultado deve conter o motivo por item. A carga parcial não é promovida silenciosamente.

### 3.3 Avisos que não recusam o item

- `price = null`: exibir `consulte`;
- `condominium_fee = null` ou `iptu = null`: exibir `não informado`;
- `media_urls = []` por ausência na exportação: `pending_manual_registration`;
- `stale_review`: aceitar no catálogo se os critérios duros passarem, mas incluir na lista de
  revisão periódica;
- qualquer coluna não mapeada: não copiar para o catálogo mínimo e registrar a pendência do
  dicionário, sem inventar significado.

## 4. Recibo, versionamento e rollback lógico

### Recibo

Cada submissão produz um `catalog_import_receipt` append-only com:

- `import_id`;
- `catalog_version`;
- `source_ref` e `cutoff_date`;
- `content_hash`;
- responsável e horário;
- totais: `rows_total`, `accepted`, `pending`, `rejected`;
- lista de motivos por linha;
- `promotion_status`: `validation_only`, `promoted`, `rejected` ou `rolled_back`.

Nesta F2-T01 a prova é `validation_only`: nenhuma versão real é promovida.

### Versão e idempotência contratual

- `catalog_version` é derivada deterministically de `cutoff_date` + hash canônico do conteúdo,
  não do `import_id`.
- Repetir o mesmo conteúdo normalizado com outro `import_id` retorna recibo idempotente e não cria
  segunda versão materialmente igual.
- Uma versão aceita é imutável. Alteração de imóvel gera novo lote/versão e diff rastreável.
- O ativo aponta para uma única versão aceita mais recente; versão anterior permanece recuperável.

### Rollback lógico

- Só o papel autorizado pode promover ou fazer rollback.
- Rollback exige motivo, ator, horário e referência da versão restaurada.
- O sistema marca a versão substituída como `rolled_back`/`superseded`, preserva seus recibos e
  derivados históricos, e reativa a versão anterior por referência.
- Nenhum registro é apagado para fazer o rollback parecer uma carga limpa.

A implementação executável desses comportamentos e a prova de permissão são critérios da F2-T02;
este documento fixa o contrato que a implementação deve cumprir.

## 5. Fixture e evidência desta task

- Fixture: `04_fase-atual/fixtures/catalogo-f2-t01.json`.
- Validador: `04_fase-atual/scripts/validar-f2-t01.py`.
- Relatório: `06_notas/fase-2/relatorio-f2-t01.md`.
- Recibo sintético: `06_notas/fase-2/recibo-f2-t01.json`.

A fixture cobre: registro válido com campos monetários zero e mídia ausente; registro desatualizado
que permanece aceito com flag; campo obrigatório ausente; vigência inválida; e mídia insegura
informada como enriquecimento manual. Não contém PII real, credenciais ou dados de cliente.

## 6. Limites e gates seguintes

- Não há API ou scraping Kenlo nesta task.
- Não há importação de um `.xls` real nesta task.
- O dicionário dos cabeçalhos restantes das 29 colunas deve ser confirmado a partir da primeira
  exportação real antes de promover lote real.
- B2-03 (acesso independente ao Skip/evidência exportável) permanece gate da F2-T02.
- A F2-T02 só pode começar depois do aceite humano desta F2-T01 e da verificação de acesso/prova.
