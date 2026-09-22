# AP-2026-09-22-0915 — comando reproduzível deve ser executado como bloco publicado

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T01 / SPEC-2-001
- Sinal: o relatório tinha um caminho de fixture diferente do caminho canônico do repositório; uma montagem auxiliar também mascarou a execução ao truncar `python3`.
- Evidência: `06_notas/debug/debug-2026-09-22-f2-t01-caminho-comando.md`; bloco de quatro linhas do relatório executado literalmente com PASS.
- Regra reutilizável: depois de gerar um comando reproduzível, verificar o texto publicado e executá-lo literalmente, sem reconstruí-lo por transformação de shell.
- Quando aplicar: toda task que entrega comandos multiline para teste humano.
- Quando não aplicar: comandos que não são entregues ao cliente ou que não têm caminhos relativos publicados.
- Confiança: alta — a falha foi reproduzida, corrigida e o mesmo bloco passou sem transformação.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.
