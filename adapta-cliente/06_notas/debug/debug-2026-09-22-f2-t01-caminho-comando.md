# Debug Summary — F2-T01

- **Sintoma:** o comando reproduzível publicado no relatório usava `04-fase-atual` (hífen), mas o caminho canônico do repositório é `04_fase-atual` (underscore).
- **Reprodução:** execução do bloco publicado falhou com `FileNotFoundError` no caminho com hífen.
- **Causa raiz:** literal de caminho incorreto na função que gera a seção de comando do relatório; o validador e os artefatos não eram a causa.
- **Correção:** substituído somente o caminho da fixture no gerador e relatório; contrato, fixture e regras não foram alterados.
- **Verificação:** comando documentado executado literalmente com `PASS`; `catalog_version=cat-20260915-fac83f9cf10a`, `content_hash=fac83f9cf10a55b9410066fd0061b28b36651131a7569f9ea67ebef6dd18c3cd`, totais 5/2/1/2; Python, JSON e `git diff --check` passaram.
- **Limite:** uma tentativa auxiliar de montar o comando via `sed` truncou `python3` para `pytho`; foi descartada e não é o comando entregue.
