# AP-2026-09-10 — card_version consistente na demonstração de ficha

- Status: candidato
- Escopo: projeto do cliente
- Task/SPEC: F1-T15 / SPEC-1-003
- Sinal: a demonstração manual comparou preview, envio registrado e repetição idempotente da mesma ficha.
- Evidência: teste humano aprovado por Janeide; repetição retornou "duplicado" sem segundo vínculo e não foi observada divergência de `card_version`.
- Regra reutilizável: em qualquer demonstração de envio idempotente, comparar a versão do preview com o resultado do envio e confirmar a repetição antes de aprovar.
- Quando aplicar: sempre que o preview gerar uma versão usada como chave de dedupe.
- Quando não aplicar: não inferir consistência para alterações posteriores da ficha sem novo teste.
- Confiança: média — validação manual da vertical de teste, sem substituir prova automatizada de hash.
- Privacidade: sem segredo, dado pessoal ou conteúdo bruto
