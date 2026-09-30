# Estado atual — Adapta Cliente

- task_id: F2-T02
- champion: Matheus Silva
- spec: 04_fase-atual/specs/spec-fase-2-001-catalogo-carga-vigencia.md
- etapa: aguardando_teste_humano
- autorizacao_implementacao: confirmada por Janeide em 2026-09-28 + "Autorizo a implementação da F2-T02"; fixture sintética apenas; Skip 55154 não publicado; V1→V2 sintética alterada→rollback V2→V1; Admin promove/corrige/rollback; SDR/Corretor somente leitura; `.xls` real fora; F2-T03 não iniciar
- teste_humano: pendente — provas runtime automatizadas PASS; Janeide ainda precisa validar UI e regressão F1 no preview
- verificacao_automatica: QA Skip 0.0.75 PASS (setup/static/build/integrations/test); migrations 0028/0029 aplicadas; suíte sintética 19/19 PASS: import/hash/totais V1, idempotência, duplicata por conteúdo, promoção V1, 2 itens ativos, falha parcial atômica sem troca de ativo, V2 distinta, promoção V2, rollback V2→V1, SDR/Corretor login/leitura/403; V1 ativa ao final
- aprendizado: capturado:06_notas/aprendizado-continuo/AP-2026-09-28-1620-falsos-zero-pocketbase.md
- ultima_acao: versão Skip 0.0.75 criada; rotas diagnósticas retornam 404; secrets temporários removidos; projeto 55154 continua não publicado
- proxima_acao: Janeide executar o roteiro humano atualizado no preview, validar interface e regressão F1; não iniciar F2-T03
- atualizado_em: 2026-09-28T16:19:55-03:00
