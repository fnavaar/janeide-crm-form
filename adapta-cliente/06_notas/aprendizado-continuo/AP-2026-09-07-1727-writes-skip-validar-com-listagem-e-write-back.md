# AP-2026-09-07-1727-writes-skip-validar-com-listagem-e-write-back

**Task:** F1-T10 (permissões, auditoria e dados incompletos do painel — SPEC-1-002)
**Data:** 2026-09-07

## Sinal reutilizável

Durante a F1-T10, múltiplos `skip_file_write` retornaram `written: true` mas o arquivo **não
persistiu** no working tree (detectado pela listagem de arquivos e confirmado pela leitura de
volta). Um segundo write saiu com trechos corrompidos (tokens repetidos/inválidos) que o QA
estático não teria pegado antes de um deploy quebrado.

## Orientação

1. **Após todo `skip_file_write`, confirmar persistência** — para arquivos críticos (migrations,
   hooks), ler de volta ou conferir na listagem do projeto antes do `apply_changes`.
2. **Migration "aplicada" não prova efeito**: uma migration idempotente que depende de secret
   pode aplicar com sucesso e não ter criado nada (ex.: secret ausente/propagação). Confirmar o
   efeito esperado (usuário criado, campo atribuído) por via indireta (teste do comportamento).
3. **Lookup de seed por chave canônica pode falhar silenciosamente**: a 0018 buscou
   `lead_id='lead-001'`; se o registro existir com outra chave, a migration "passa" sem efeito.
   Migrations de atribuição devem ter fallback (ex.: busca por nome) e logar o resultado.
4. **Diagnóstico de "não apareceu no frontend"**: confirmar (a) código no bundle publicado,
   (b) resposta real do endpoint, (c) cache do navegador — nessa ordem, antes de alterar código.
