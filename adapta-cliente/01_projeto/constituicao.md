# Constituição do projeto — Imobiliária Janeide Xavier LTDA

> Regras estáveis deste projeto. Valem em todas as fases e só mudam por decisão registrada da
> consultoria (emenda datada na seção final). Mantida pela consultoria — dúvida vira registro
> no `changelog.md`, não edição. (Conceito adaptado do Spec Kit, decisão D18.)

## Papéis

- **Champion:** Matheus Silva — executa as tasks da fase atual e valida com evidência.
- **Consultor Adapta:** Adapta Labs — define escopo, SPECs e critérios; fecha as fases.
- **Agente (Claude):** guia a execução dentro destas regras; não legisla sobre escopo.

## Stack e ferramentas permitidas

- WhatsApp Business ou plataforma central autorizada, CRM, fonte de catálogo aprovada, painel operacional e ambiente de testes definido nas SPECs.
- Kenlo/Quelo/site, agenda e conectores só entram como fonte depois da validação registrada na task correspondente.
- Dependência ou ferramenta nova só entra por decisão do consultor — registre `DÚVIDA:` antes.

## O que o champion pode e não pode tocar

- **Pode:** executar as tasks elegíveis em `04_fase-atual/`, registrar evidências em `STATUS.md` e `changelog.md`, e criar notas em `06_notas/`.
- **Não pode:** specs, `fase.md` (além de marcar tasks), `01_projeto/`,
  fontes de produção, agenda, reservas, credenciais, políticas de consentimento ou envio de mensagens sem autorização prevista na SPEC.

## A SPEC é lei

Toda implementação segue o critério de aceite e o TDD da SPEC — nem menos (critério reprovado),
nem mais (**o aceite é teto**: código além do aceite é superfície não verificada, D17). O que
não está na SPEC da fase não se implementa: vira `DÚVIDA:` para o consultor decidir.

## Linha vermelha (nunca simplificar)

Validação de entrada em fronteira de confiança; tratamento de erro que evita perda de dados;
segurança; acessibilidade; LGPD/dados pessoais. Corte nessas áreas reprova a task — sem exceção
e sem julgamento de mérito (D17).

## Dívida deliberada

Simplificação intencional leva marca no ponto exato da decisão:
`adapta-divida: <teto atual>; <upgrade quando gatilho>`. O consultor acompanha essas marcas na
sincronização — é o combinado do método.

## Emendas

| Data | O que mudou | Decisão/motivo |
|---|---|---|
| | | |
