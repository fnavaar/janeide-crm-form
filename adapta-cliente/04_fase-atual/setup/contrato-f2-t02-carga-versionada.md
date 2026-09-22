# Contrato de carga versionada — F2-T02

**Task:** F2-T02 — Implementar carga versionada, idempotência e rollback lógico  
**SPEC:** SPEC-2-001 — Catálogo mínimo, carga e vigência  
**Estado:** B2-03 resolvido no recorte técnico; implementação da carga ainda não iniciada  
**Ambiente de prova:** Skip Cloud — projeto `55154` — **Janeide Teste Fase 1**  
**Preview:** `https://janeide-teste-fase-1-ba587--preview.goskip.app`  
**Produção:** `https://janeide-teste-fase-1-ba587.goskip.app` — projeto não publicado; não usar produção  
**Backend de teste:** `https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev`  

## 1. Conta técnica dedicada — B2-03

A conta técnica de auditoria foi provisionada no projeto Skip 55154 para permitir prova independente da F2-T02 sem acesso a produção nem a dados reais de cliente.

- **Identidade:** `Auditoria F2-T02` (`f2-t02-audit@janeide.test`).
- **Credencial:** armazenada exclusivamente no secret do Skip `AUDIT_F2_T02_CREDENTIALS`; o valor não é versionado, não aparece neste contrato e não deve ser enviado no chat.
- **Papel técnico no ambiente de teste:** `admin` na collection de usuários do projeto 55154.
- **Migration:** `pocketbase/migrations/0024_f2_t02_audit_account.js`.
- **Migration aplicada:** `0024_f2_t02_audit_account`, versão `1790087075`.
- **Versão Skip após aplicação:** `0.0.61` (`8d659d9`).
- **QA observado:** setup, análise estática, build, integrações e testes — todos PASS.

## 2. Escopo técnico da permissão

A conta pode, no ambiente de teste 55154:

- autenticar como usuário técnico dedicado;
- ler o catálogo de propriedades de teste;
- criar, corrigir e remover registros da collection `properties`, porque suas regras de escrita exigem `@request.auth.role = 'admin'`;
- ser usada como ator técnico nas futuras provas de importação, promoção controlada e rollback da F2-T02, quando essas superfícies forem implementadas.

A conta **não** recebe:

- acesso a produção — o projeto 55154 está `isPublished: false`;
- dados reais de clientes — a prova deve usar somente fixtures/snapshots sintéticos ou minimizados autorizados;
- acesso amplo à collection de usuários — a regra de `users` continua limitada ao próprio usuário;
- autorização automática de negócio para promover, corrigir ou executar rollback em nome da operação.

## 3. Limite entre capacidade técnica e autoridade de negócio

A migration 0024 fornece a capacidade técnica mínima para a prova independente. Ela não decide quem é o aprovador humano nem autoriza promoção de versão real.

**Decisão pendente seguinte:** definir qual papel/conta é a autoridade de negócio autorizada a promover uma versão, corrigir lote e executar rollback. Até essa decisão, a F2-T02 não deve promover catálogo nem executar rollback operacional.

## 4. Fora do recorte já executado

Ainda não foram implementados nem provados:

- parser/carga versionada;
- collections de versões/recibos, se necessárias;
- promoção controlada;
- idempotência de lote;
- falha parcial/reprocessamento;
- rollback lógico;
- teste humano da F2-T02.

A F2-T01 permanece a fonte contratual para formato, normalização, retenção, log e critérios de catálogo.

## 5. Segurança e recuperação

- Não colocar senha ou token em migration, contrato, changelog, fixture ou mensagem.
- Se a conta técnica for comprometida, rotacionar o secret `AUDIT_F2_T02_CREDENTIALS` e executar uma migration de atualização de senha; não publicar o valor.
- Não usar rollback de migration para desfazer a conta em banco de teste sem preservar o histórico da prova; qualquer reversão deve ser deliberada e registrada.
