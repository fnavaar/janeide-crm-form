# Debug Summary — F1-T14

- **Sintoma:** corretor sem atribuição recebia auditoria vazia sem explicação visual.
- **Reprodução:** rota de auditoria negava acesso, mas o frontend não preservava o status HTTP e renderizava o mesmo estado de lista vazia.
- **Causa raiz:** `listAudit()` propagava erro sem tratamento específico; o componente não distinguia 403 de resposta 200 com zero eventos.
- **Correção:** frontend passou a preservar 403 e exibir “Sem permissão para ver a auditoria deste lead”; 200 vazio continua “Sem eventos de auditoria”.
- **Verificação:** Skip 0.0.59 / 7f72ecd, QA verde; teste humano confirmou SDR com 2 eventos, corretor com telefone oculto e mensagem explícita de permissão, além da distinção de estados.
