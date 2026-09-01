# Contrato de Setup — Catálogo e Ficha de Imóvel (F1-T03)

**Task:** F1-T03 — Fechar fonte do catálogo, campos, vigência e mídia
**SPEC:** SPEC-1-003
**Dono:** Matheus Silva
**Criado em:** 2026-08-26 por Janeidinha
**Estado:** CONFIRMADO (2026-08-31) — itens 1 a 6 confirmados

> Este documento registra as decisões que precisam ser fechadas para destravar a leva 5 da Fase 1
> (F1-T07). Cada item tem dono, estado e o que precisa para fechar. Nenhum item pode ser presumido
> ou inventado — ausência de decisão vira bloqueio registrado. Replica o padrão de
> `contrato-captura.md` (F1-T01) e `contrato-painel.md` (F1-T02).

## Itens de decisão

### 1. Fonte de verdade do catálogo

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** **Kenlo Mob** é a fonte de verdade atual do catálogo de imóveis. Nesta
  fase, o painel próprio (Skip Cloud) mantém um **catálogo mínimo replicado** a partir do Kenlo
  (opção A) — **sem depender de API/homologação** externa para leitura. "Quelo" é apenas
  pronúncia de "Kenlo", não um sistema separado.
- **Carga inicial:** via **exportação/importação manual (planilha)** do catálogo atual da Kenlo.
  O painel (backend PocketBase do Skip) **suporta importação em lote** (seed/migration ou
  importação administrativa de dados); o mecanismo exato será definido na implementação
  (F1-T07). **Preferência: importação em lote** — não cadastro imóvel por imóvel. *Nota: o
  painel ainda não foi construído; a capacidade de batch será implementada junto com a fila.*
- **Modelo operacional temporário (registrado):** enquanto Kenlo e painel rodam **em paralelo**,
  a **atualização de status/preço é feita manualmente nos dois lugares** — rotina operacional da
  equipe, **não** issue técnico; válida até a fase de substituição da Kenlo.

### 2. Acesso de leitura

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** o acesso de leitura fica **restrito ao catálogo mínimo replicado no
  painel** (Skip Cloud) — **sem credenciais de API da Kenlo** nesta fase. **SDR e sistema leem a
  ficha diretamente do painel**, sem homologação externa.

### 3. Campos mínimos

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** os **10 campos da SPEC** são o modelo do catálogo mínimo no painel:
  `property_code`, `title`, `availability_status`, `price`, `condominium_fee`, `iptu`,
  `key_attributes`, `media_urls`, `source_ref`, `valid_until`.
- **Regras de obrigatoriedade (aprovadas):**
  - `price` — **obrigatório quando a operação tiver valor definido**; pode haver casos "consulte"
    (sem valor) que são válidos e devem ser exibidos como tal, sem inventar;
  - `condominium_fee` / `iptu` — **opcionais**, sem preenchimento inventado (RN-3: ausente vira
    pendência, não valor fictício);
  - `valid_until` — **obrigatório para vigência**, conforme RN-1 (sem vigência, bloquear
    automatização);
  - `source_ref` — obrigatório (origem da ficha/versão da carga);
  - `property_code`, `title`, `availability_status` — obrigatórios para exibir a ficha.
- **Para fechar:** revisar formatos/tamanhos destes campos contra o modelo de dados do painel na
  implementação (F1-T07); nenhum campo fora desta lista no catálogo mínimo.

### 4. Vigência / validade

- **Dono:** Matheus Silva / responsável de cadastro (papel — item 6)
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada — regra de vigência:**
  - `valid_until` vem da **carga inicial** (planilha do Kenlo); imóvel sem vigência confirmada
    **bloqueia automatização** (prévia/envio automático) — só manual, com revisão humana;
  - imóvel **vencido** bloqueia preview/envio (RN-2), com **motivo visível ao SDR** (CA-1-11);
  - renovação de vigência feita **manualmente no painel** pelo responsável de cadastro (papel),
    quando renegociar na Kenlo (mesma rotina de status/preço em paralelo).
- **Adicional — lista de vencidos/pendentes de revisão:** quando um imóvel vencer, ele deve
  aparecer numa **lista visível** (ex.: "imóveis vencidos / pendentes de revisão") para o
  **responsável de cadastro** — sem esse aviso, o bloqueio pode passar despercebido por tempo
  indefinido até alguém notar manualmente. Essa lista é parte do painel (fila de pendências).

### 5. Mídia / envio por WhatsApp

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada — envio do card:**
  - o card da ficha é enviado **manualmente pelo SDR, pelo número atual de atendimento** (app
    comum, **fora da API**) — fluxo que o SDR já conhece, com histórico e confiança estabelecida;
  - o sistema **registra o vínculo do envio**: lead, imóvel, versão da ficha, usuário que enviou,
    horário (e `message_ref` quando disponível) — **sem enviar automaticamente via API**.
- **Por que não via API no número de captura:** um número na Cloud API **não pode também ser
  usado no app comum** (são exclusivos); enviar pelo número de captura exigiria construir uma
  interface de envio no painel (trabalho técnico novo, fora do escopo fechado até agora). A
  escolha pelo número atual é **por simplicidade e continuidade de confiança com o cliente**,
  não limitação técnica não avaliada.
- **RN-5 — Mídia segura:** exibir somente mídia da fonte aprovada (Kenlo → catálogo mínimo); URL
  arbitrária/insegura **bloqueia o card**; URLs de mídia tratadas como dado.

### 6. Responsável pela atualização do catálogo

- **Dono:** Matheus Silva / Janeide Xavier
- **Estado:** **CONFIRMADO** (2026-08-31)
- **Decisão fechada:** o papel responsável por manter/corrigir os dados do catálogo é o
  **responsável por cadastro/imóveis** — **sem nomear pessoa específica** (pode mudar; mesma
  lógica do contrato-painel item 6). Esse papel também renova `valid_until` e corrige dados
  incompletos/divergentes na fonte (CA-1-11/cenário "Incompleto").

## Regras de negócio a validar no contrato

- **RN-1 — Fonte vigente:** exibir `source_ref` e vigência; sem vigência, bloquear automatização.
- **RN-2 — Disponibilidade:** só liberar preview com status ativo confirmado.
- **RN-3 — Dados comerciais:** exibir preço/taxa exatamente da fonte; ausente/divergente vira
  pendência; **não inventar preço, taxa, entrega ou decorado**.
- **RN-4 — Envio humano:** SDR confirma; envia uma vez e registra; sem confirmação não envia.
- **RN-5 — Mídia segura:** só mídia da fonte aprovada; URL arbitrária/insegura bloqueia o card.

## Fixture de teste

O fixture `imovel-001` será validado quando o ambiente for confirmado. Não contém PII real.

## Próximo passo

Realizar a **call de setup** com Matheus Silva (e Janeide Xavier quando aplicável) para fechar os
itens acima. Cada decisão fechada deve ser registrada neste documento e no `changelog.md`.
Itens não resolvidos permanecem como bloqueio registrado em `STATUS.md`.