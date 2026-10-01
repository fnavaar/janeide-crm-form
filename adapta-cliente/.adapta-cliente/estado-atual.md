# Estado atual — Adapta Cliente

- task_id: F2-T04
- champion: Matheus Silva
- spec: 04_fase-atual/specs/spec-fase-2-002-busca-ficha-vigente.md
- etapa: bloqueada
- autorizacao_implementacao: confirmada por Janeide em 2026-10-01 13:18 ("Pode retomar: aplicar a migration 0031 e seguir com a F2-T04"); o bloqueio atual é dúvida de escopo CA-2-012, não falta de autorização para o recorte original
- teste_humano: pendente — não iniciar login/papel até Janeide/consultor fechar se CA-2-012 exige negar acesso integral à PII do lead (`email` e demais campos) para `outro`, além de ocultar telefone conforme matriz F1
- verificacao_automatica: parcial — Skip 55154 v0.0.86 (`aeb20a3`) QA setup/static/build/integrations/test 5/5 PASS após role gate em `pocketbase/hooks/ficha.js`; migration `0031_f2_t04_outro_test_account` aplicada; GET sem token para ficha e busca retornou 401 e logs correspondentes. Não executada prova autenticada `role=outro`/403, nem prova SDR/Admin ficha 200. CA-2-010/011 ainda sem matriz automatizada. Projeto preview não publicado; `.skip.config.json` preexistente permanece pending.
- aprendizado: pendente
- ultima_acao: role gate admin/sdr/corretor acrescentado à ficha antes da busca e validado por QA; inspeção read-only revelou que hook do cartão retorna email/outros campos para papel outro e coleção leads aceita qualquer usuário autenticado; documentação local de segurança/changelog/STATUS atualizada; nenhuma credencial lida/alterada
- proxima_acao: Janeide decidir com consultor o alcance de CA-2-012/PII para papel outro antes de prosseguir com teste autenticado; não iniciar F2-T05
- atualizado_em: 2026-10-01T13:49:00-03:00
