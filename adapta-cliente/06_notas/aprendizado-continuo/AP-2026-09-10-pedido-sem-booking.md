# AP-2026-09-10 — demonstração de pedido sem booking

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T16 / SPEC-1-004
- Sinal: a demonstração manual confirmou pedido pendente, deduplicação, esclarecimento de janela, ausência de booking e cancelamento com histórico.
- Evidência: teste humano aprovado por Janeide nos cinco cenários da F1-T16.
- Regra reutilizável: ao demonstrar uma jornada de visita sem agenda integrada, provar explicitamente tanto o estado recuperável quanto a inexistência de slot, corretor, chave ou reserva.
- Quando aplicar: em qualquer handoff de pedido entre uma fase sem agenda e uma fase futura com agenda.
- Quando não aplicar: não tratar a ausência de botão na UI como única prova se houver backend ou coleção de booking não inspecionados.
- Confiança: alta — cinco cenários manuais confirmados e backend/coleções inspecionados na análise.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto
