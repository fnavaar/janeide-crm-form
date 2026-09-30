# Debug F2-T02 — cartão de bloqueio SDR/Corretor duplicado

- Data: 2026-09-30
- Task/SPEC: F2-T02 / SPEC-2-001
- Ambiente: Skip 55154, preview não publicado

## Sintoma e reprodução

Durante o teste humano B/SDR no preview 0.0.75, Janeide informou duas seções quase idênticas, cada uma com um botão de promoção. A primeira tentativa de promoção retornou HTTP 403: `Somente Admin pode promover uma versão.` O log de requests do Skip confirma o POST `/backend/v1/catalogo/promover` com status 403.

## Causa raiz confirmada

`src/pages/CatalogoF2T02.tsx` continha dois blocos `<Card>` consecutivos sob a mesma condição `!isAdmin && (role === 'sdr' || role === 'corretor')`. Ambos renderizavam botões que chamavam `tryPromotionAsReadOnly()`. Era duplicação de UI, não falha de autorização do backend.

## Correção

Removido somente o segundo cartão; o primeiro, a condição de papel e o handler do botão foram preservados. Nenhuma rota/backend, coleção, migration ou dado foi alterado.

## Verificação automática

- Leitura de volta de `src/pages/CatalogoF2T02.tsx`: uma ocorrência do cartão de bloqueio, uma ocorrência do botão renderizado e uma condição para SDR/Corretor — PASS.
- Skip QA/build v0.0.76 (`d69136f`): setup, análise estática, build, integrações e testes — PASS.
- `isPublished=false`; nenhuma publicação de produção executada.
- `.skip.config.json` foi aceito por Janeide como pendência antiga para o finalize de desenvolvimento; após o build, o Skip ainda o lista em `pendingChanges`, e o seu `deployment.lastDevBuildRef` é `d69136f`.

## Gate humano

O 403 do SDR foi comprovado no preview anterior 0.0.75; A2 e A4 foram aprovados. A interface corrigida ainda aguarda conferência humana. Próximo passo único: entrar como Corretor no preview 0.0.76, confirmar leitura da V1 e dois itens, confirmar apenas um cartão/botão, clicar uma vez e observar HTTP 403. Depois retomar C e D. F2-T02 permanece aberta; F2-T03 não iniciar.
