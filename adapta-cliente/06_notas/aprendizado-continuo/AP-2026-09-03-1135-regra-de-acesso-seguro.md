# AP-2026-09-03-1135 — acesso de teste nunca deve ser exibido no chat

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T06 / SPEC-1-002
- Sinal: para destravar o login do painel, o agente gerou uma senha de teste e a colou em texto puro na resposta do chat. A cliente apontou que isso quebra a regra de acesso aprovada, mesmo em teste.
- Regra reutilizável: nunca gerar e exibir dado de acesso no chat, arquivo ou documento. O usuário define o valor diretamente no mecanismo de guarda e confirma apenas a troca; o agente valida sem ver o valor.
- Quando aplicar: qualquer task que precise de acesso de teste/usuário.
- Confiança: alta.
- Privacidade: sem valor de acesso, dado pessoal ou conteúdo bruto.
