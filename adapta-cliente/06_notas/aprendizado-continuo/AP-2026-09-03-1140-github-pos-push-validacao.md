# AP-2026-09-03-1140 — validar conteúdo publicado no GitHub após push via MCP

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T06 / fechamento; aplicável a toda sincronização GitHub
- Sinal: ao publicar `04_fase-atual/fase.md` via `mcp_github_create_or_update_file`, o conteúdo foi **re-digitado manualmente no payload** e saiu com typos ("reslovida", "quatr ss tas", "acete"...), corrompendo o arquivo remoto. A API do GitHub não valida conteúdo — só grava. Arquivos grandes vizinhos (changelog 14 KB, specs 11 KB) publicados pelo mesmo canal saíram íntegros, confirmando causa humana de transcrição, não encoding/truncamento.
- Regra reutilizável: ao publicar qualquer arquivo no GitHub via MCP (create_or_update_file / push_files), **ler de volta o arquivo remoto após o push e comparar com o local** (ou conferir trechos críticos/hashes) antes de reportar "sincronizado". Preferir edições curtas/patch. Código do Skip não passa por esse caminho (escrita direta no working tree + QA com build/static analisa sintaxe).
- Quando aplicar: toda sincronização GitHub de documentos no projeto (fase.md, STATUS, changelog, contratos, specs).
- Quando não aplicar: escrita no Skip Cloud (validação via QA).
- Confiança: alta — incidente real com correção imediata (commit 6968e25 restabeleceu o conteúdo íntegro).
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto.