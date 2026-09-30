# Contrato de carga versionada — F2-T02

**Task:** F2-T02 — Implementar carga versionada, idempotência e rollback lógico  
**SPEC:** SPEC-2-001 — Catálogo mínimo, carga e vigência  
**Estado:** implementação autorizada; em correção antes do teste humano devido a falha runtime na importação V1; decisões desta task fechadas  
**Dados de prova:** exclusivamente fixtures sintéticas  
**Ambiente:** Skip Cloud, projeto `55154` — **Janeide Teste Fase 1**, não publicado  
**Rollback de prova:** promover V1 → promover V2 sintética alterada → rollback V2 → V1  
**Preview:** `https://janeide-teste-fase-1-ba587--preview.goskip.app`  
**Backend de teste:** `https://janeide-teste-fase-1-ba587.shrd00.internal.goskip.dev`  

## 1. Decisões fechadas

- A primeira prova usa somente a fixture sintética aprovada na F2-T01 e uma derivação sintética V2 com alterações identificáveis. Não será aberto nem importado um arquivo `.xls` real nesta task.
- A sequência obrigatória no Skip 55154 é: **V1 (fixture F2-T01) → V2 (fixture sintética alterada) → rollback lógico para V1**.
- As versões, recibos, itens normalizados e histórico de operações devem permanecer consultáveis depois da promoção e do rollback; rollback não apaga versões nem recibos.
- Uma carga repetida com o mesmo conteúdo canônico é idempotente: não cria nova versão material nem duplica itens.
- Lote com linhas recusadas/pendentes ou falha técnica não pode trocar silenciosamente a versão ativa. Admin deve receber totais e motivos; a falha mantém a versão ativa anterior. Só itens classificados e explicitamente aprovados para ativação entram no catálogo.

## 2. Autoridade e permissões de negócio

- **Único papel autorizado:** **Admin** pode importar, corrigir lote, promover versão e executar rollback lógico, com revisão e registro de cada ação.
- A regra é pelo papel, não por pessoa. Matheus ocupa atualmente o papel Admin; a troca do ocupante não altera este contrato.
- **SDR e Corretor:** leitura do catálogo e dos resultados necessários à operação; sem criar, alterar, importar, corrigir, promover ou executar rollback.
- As permissões devem ser verificadas no backend/RLS, não apenas ocultando botões na interface.

## 3. Conta técnica de auditoria — somente prova

A conta `Auditoria F2-T02` (`f2-t02-audit@janeide.test`) existe exclusivamente no projeto de teste 55154 para comprovar o comportamento técnico. Seu papel `admin` nesse ambiente isolado simula a trilha autorizada de teste; **a conta não tem autoridade de negócio, não é aprovadora e não representa o Admin operacional**.

- Credencial somente no secret Skip `AUDIT_F2_T02_CREDENTIALS`; nunca versionar ou publicar o valor.
- Migration que a provisionou: `pocketbase/migrations/0024_f2_t02_audit_account.js` (aplicada; versão Skip `0.0.61`, hash `8d659d9`).
- A conta deve permanecer confinada ao 55154 não publicado e a fixtures sintéticas.
- **Gate obrigatório antes de qualquer uso em produção:** remover ou desativar esta conta e confirmar que não existe no ambiente produtivo; não copiar o secret de teste para produção.

## 4. Fluxo e invariantes

1. Validar entrada fixture, campos, vigência, mídia permitida e classificações; calcular hash canônico no servidor.
2. Persistir versão em estágio, linhas normalizadas/classificadas e recibo append-only; não mudar a versão ativa durante importação.
3. Repetição do mesmo hash/request id retorna o resultado anterior sem criar versão material duplicada.
4. Admin revisa o recibo e promove explicitamente uma versão completa. Candidato recusado ou pendente não vira item ativo.
5. Promoção e alterações do catálogo vivo executam atomicamente; erro em qualquer item reverte a transação inteira e preserva a versão anterior ativa.
6. Rollback V2 → V1 reativa o snapshot imutável de V1 e restaura os itens correspondentes; V2 passa a estado revertido, mas versões, recibos e histórico permanecem.
7. Ações de SDR/Corretor para mutação retornam 403 e não alteram versões, catálogo ou recibos de operação.

## 5. Escopo e limites

- **Inclui:** carga do formato de fixture sintética, validação/normalização mínima necessária, hash e idempotência, recibos, versões imutáveis, promoção controlada, falha atômica, auditoria de permissões e rollback lógico V2→V1.
- **Não inclui:** leitura ou parser de `.xls` real, ingestão de dados de clientes, conexão ao Kenlo, publicação em produção ou F2-T03 (busca nova por código/bairro/tipo).
- A fixture F2-T01 é prova de validação com 5 linhas (2 aceitas, 1 pendente, 2 recusadas); somente candidatos aceitos podem ser materializados como propriedades ativas. O restante fica registrado com classificação e motivo.

## 6. Critérios binários para teste

- **Idempotência:** mesmo hash em nova tentativa não cria uma segunda versão material nem duplica propriedades.
- **V1/V2:** V1 reproduz `cat-20260915-fac83f9cf10a`; V2 deriva da fixture sintética e tem hash/conteúdo distintos; cada recibo apresenta totais e ator.
- **Promoção/falha parcial:** importação não altera catálogo ativo; promoção explícita é atômica; falha parcial ou recusada mantém versão anterior ativa, sem resíduo parcial.
- **Permissões:** Admin de prova pode operar; SDR e Corretor conseguem ler e recebem 403 ao tentar mutação; nenhum estado é alterado pelas tentativas negadas.
- **Rollback:** depois de V2 ativa, rollback aponta V1, os campos ativos voltam a corresponder exatamente ao snapshot de V1 e o histórico de V2/recibos continua preservado.
- A F2-T02 para em `aguardando_teste_humano`; não iniciar F2-T03 até aprovação humana.
