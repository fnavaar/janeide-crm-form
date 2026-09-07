# AP-2026-09-03-1135 — credencial de teste nunca deve ser exibida no chat

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T06 / SPEC-1-002
- Sinal: para destravar o login do painel, o agente gerou uma senha de teste e a colou em texto puro na resposta do chat. A cliente (Matheus/Janeide) apontou que isso quebra a regra de credenciais aprovada em 2026-09-01, mesmo em ambiente de teste e sob pressão de tempo. A senha exposta no histórico foi tratada como comprometida e precisou ser trocada.
- Regra reutilizável: **nunca** gerar e exibir uma credencial (nem de teste) no chat, em arquivo ou em documento. Quando uma credencial precisar existir: o usuário define o valor diretamente no secret (`Skip Cloud → Segredos`), avisa apenas "troquei", e o agente recria o usuário via migration que lê `$secrets.get(...)` — sem que o valor trafegue pelo agente ou pelo chat. Validação da troca sem ver o valor: confirmar que a senha antiga deixou de funcionar (status 400) e pedir que o usuário confirme o login novo.
- Quando aplicar: qualquer task que precise de credencial de teste/usuário (F1-T06+ e fases futuras).
- Quando não aplicar: nenhum caso — a regra vale sem exceção.
- Confiança: alta — correção explícita da cliente.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
