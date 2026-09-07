# AP-2026-09-07-1815-campo-json-em-goja-nao-e-array-js

**Task:** F1-T11 (bloqueios de catálogo, mídia e envio duplicado — SPEC-1-003)
**Data:** 2026-09-07 (rev3)

## Sinal reutilizável (atualizado após 3 deploys e prova matemática)

Em hooks da Skip (runtime goja), `record.get('campo_json')` de um campo **JSON** pode voltar como
**array de BYTES** (código numérico por caractere do texto JSON) — não como array de strings nem
string JSON. **Prova:** o painel reportava "84/142/78 URLs inseguras" — exatamente os
`JSON.stringify(media_urls).length` dos três seeds (match 3/3). Iterar esse valor com `for..of`
produz um "item" por byte.

## Sintoma → causa

- **Contagens absurdas e idênticas entre deploys** = o valor é determinístico (formato do dado),
  não código velho nem cache. Antes de culpar reload/infra, calcular o que os números significam.
- `typeof`/`Array.isArray` não bastam: array de bytes **é** array JS (`Array.isArray === true`),
  mas seus itens são números.

## Orientação

1. **Normalizar campo JSON com detecção de bytes**: se `Array.isArray(v) && typeof v[0] === 'number'`,
   reconstruir a string com `String.fromCharCode` byte a byte e reprocessar (como string JSON).
2. Depois disso, aceitar array de strings, string JSON (`[...]`) e objeto goja
   (`JSON.stringify` ida-e-volta). Se nada encaixar → `null` → **bloqueio conservador**.
3. **Validar URL sem `new URL`** (goja): prefixo `https://` + host até a primeira `/`, minúsculas.
4. **Provar a lógica localmente antes de re-teste humano** (réplica em Node dos formatos
   possíveis) — "QA verde" do pipeline não exercita o runtime goja com dados reais.
5. Duplicação de lógica entre hooks exige correção nos dois + leitura de volta (resquício
   `safeArray` detectado em `envio.js` no write-back).
