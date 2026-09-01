# AP-2026-08-18-1058 — Tasks da leva 1 são fechamento de contrato, não código

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T01 / SPEC-1-001; aplicável a F1-T02, F1-T03, F1-T04
- Sinal: as 4 tasks da leva 1 da Fase 1 têm critério binário "X aprovados ou bloqueio registrado" e ponto de parada "parar sem implementar se fonte/chave não forem aprovadas". A implementação é documentar as decisões pendentes com dono e estado, criar fixture/evidência, e registrar bloqueio — não escrever código.
- Evidência: `04_fase-atual/fase.md` linhas F1-T01 a F1-T04 (critério e ponto de parada); `04_fase-atual/specs/spec-fase-1-001-captura-lead-origem.md` seções "Bloqueios" e "Instruções de execução" itens 5–6; `04_fase-atual/setup/contrato-captura.md` (artefato produzido)
- Regra reutilizável: ao selecionar uma task da leva 1, o plano de implementação é criar um documento de contrato de setup com cada decisão pendente (dono, estado, o que precisa para fechar) e o fixture/evidência correspondente. Não presumir que "implementar" significa escrever código. O critério aceita bloqueio registrado como resultado válido.
- Quando aplicar: ao trabalhar F1-T02 (painel), F1-T03 (catálogo) e F1-T04 (pedido de visita) — todas da leva 1, todas com "call de setup" como pré-condição.
- Quando não aplicar: tasks da leva 2 em diante (F1-T05+), que são implementação técnica e exigem RED/GREEN/REGRESSÃO.
- Confiança: alta — evidência direta na fase.md e na SPEC; padrão confirmado em 4 tasks da mesma leva.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto