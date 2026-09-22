# AP-2026-09-22-1027 — Drift de transcrição do MCP GitHub em arquivos longos

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F2-T01 / SPEC-2-001
- Sinal: tentativas de publicar o `changelog.md` longo via MCP GitHub produziram blobs remotos diferentes do arquivo local; leituras de volta confirmaram alterações de redação, espaçamento, linhas históricas e newline final. O diff local/remoto foi gerado antes do fallback.
- Evidência: blob local `2b0bdede77d821e3bf1ef8b9280b75da7a33f2e0`; blob remoto `b953d7e0d57669d13bf5bf50ed409ca1be30f6df`; patch mínimo em `artifacts/changelog-local-vs-remote.patch`; snapshots em `artifacts/changelog-final-local-2b0bdede.md` e `artifacts/changelog-current-remote-b953d7e0.md`; leitura de volta via `mcp_github_get_file_contents`.
- Regra reutilizável: tratar o blob local validado como canônico quando o conector MCP introduzir drift em documento longo; sempre ler de volta e comparar blob SHA, não declarar sincronização por semelhança semântica. Se a API não aceitar patch por hunk, registrar a limitação e não bloquear a validação técnica quando o cliente aprovar a canonicidade local.
- Quando aplicar: publicação de Markdown longo ou outro arquivo textual grande via MCP GitHub.
- Quando não aplicar: arquivos curtos ou push Git autenticado que preserve o objeto local exato.
- Confiança: alta — múltiplos envios, leituras de volta, hashes e diff reproduzível confirmaram o padrão.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto desnecessário.
