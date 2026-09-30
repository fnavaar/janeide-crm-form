# Roteiro humano atualizado — F2-T02

**Ambiente:** Skip 55154, preview não publicado: https://janeide-teste-fase-1-ba587--preview.goskip.app/f2-t02/catalogo
**Painel F1:** https://janeide-teste-fase-1-ba587--preview.goskip.app/
**Preview atual:** versão 0.0.76 (`d69136f`), QA PASS, não publicado.
**Estado inicial já preparado:** V1 (`cat-20260915-fac83f9cf10a`) ativa; V2 sintética existe no histórico e foi revertida; somente dados sintéticos.
**Não usar:** produção, `.xls` real, dados reais, WhatsApp real. Não iniciar F2-T03.

## A — Revisão do catálogo como Admin de teste

1. Abra o painel F2-T02 e entre com a conta técnica Admin já configurada no cofre do projeto. Não cole credenciais neste chat.
   - Esperado: painel carrega sem erro; papel exibido como `admin`.
2. Confira a versão ativa e os itens.
   - Esperado: ativa `cat-20260915-fac83f9cf10a`; **2 itens aceitos** no ativo.
3. Confira a lista de versões e o histórico administrativo.
   - Esperado: V1 e V2 estão preservadas; V2 aparece como revertida/substituída; registros de importação, duplicata, falha parcial, promoção e rollback continuam disponíveis. Nenhum histórico foi apagado.
4. Se desejar verificar a repetição pela interface, clique **Carregar V1** uma vez.
   - Esperado: `duplicate`/idempotente, hash da V1 igual a `fac83f9cf10a55b9410066fd0061b28b36651131a7569f9ea67ebef6dd18c3cd`, sem segunda versão material e sem alterar a versão ativa.
   - Se a UI mostrar mensagem diferente, pare e anote o texto; não tente corrigir dados.

## B — Leitura e bloqueio para SDR e Corretor

**Checkpoint 2026-09-30:** A2 e A4 aprovados. O teste SDR em 0.0.75 retornou HTTP 403 esperado; dois cartões quase idênticos foram encontrados. Janeide confirmou o clique acidental que criou apenas um recibo/operação append-only `duplicate` para V2; a chamada de falha parcial foi rejeitada com HTTP 400 antes da gravação. A V1 permaneceu ativa e não houve corrupção. A duplicação visual foi corrigida em 0.0.76 (QA PASS); continuar agora pelo passo 7 com o Corretor e verificar que há apenas um cartão.

5. Saia e entre com a conta SDR de teste; atualize o painel.
   - Esperado: lê V1 e os 2 itens ativos; não vê controles administrativos/histórico.
6. Use **Tentar promover (esperado 403)**, caso esteja disponível na tela.
   - Esperado: HTTP 403 e V1 continua ativa.
7. Entre com a conta Corretor de teste e abra esta rota no preview 0.0.76.
   - Esperado: leitura dos mesmos 2 itens; aparece uma única seção “Teste do bloqueio de escrita — CORRETOR” e um botão “Tentar promover (esperado 403)”. Clique uma vez. Esperado: HTTP 403 e V1 continua ativa, sem mudança em versões, snapshots ou recibos.

## C — Conferência de rollback sem repetir mutações

8. Volte ao Admin e confira novamente o ativo e o histórico após os papéis de leitura.
   - Esperado: V1 segue ativa; V2 continua preservada como revertida; nenhum snapshot/recibo foi apagado.
   - Não execute nova promoção/rollback se a interface indicar V1 já ativa. A prova V1→V2→V1 foi executada automaticamente e passou; este passo confirma o estado visível na UI.

## D — Regressão da Fase 1

9. Abra o painel F1 no mesmo preview e entre como SDR sintético.
10. Localize o lead sintético existente ligado ao imóvel `CASAS-TURIM-001` (não crie lead real).
    - Se não estiver na fila, pare e registre isso; não altere seeds.
11. Consulte a ficha por código `CASAS-TURIM-001`.
    - Esperado: preview válido, ficha/preço/vigência e `card_version` visíveis; sem bloqueio de vencimento, ficha incompleta ou mídia insegura.
12. Se o fluxo existente permitir, clique **Confirmar envio (registrar vínculo)**.
    - Esperado: vínculo registrado sem disparar WhatsApp. Repetir o mesmo registro deve indicar duplicidade, sem criar segundo vínculo.

## Como devolver o resultado

Informe quais partes A–D passaram. Se algo divergir, indique a parte/passo, papel usado e mensagem exibida; pare nesse passo e não tente corrigir manualmente. A F2-T02 permanece aguardando aprovação humana explícita. F2-T03 não deve ser iniciada.
