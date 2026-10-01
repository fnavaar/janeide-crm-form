# Achado de acesso à ficha e PII do lead — projeto de teste 55154

**Data:** 2026-10-01  
**Classificação atual:** achado de segurança confirmado no projeto de teste 55154; ocorrência em produção não determinada. Ficha protegida no preview 0.0.86; cobertura da PII do lead para o papel `outro` ainda pendente de decisão/validação.  
**Relação com F2-T04:** correção do role gate da ficha foi autorizada e aplicada no preview dentro da retomada F2-T04; a decisão se a CA-2-012 abrange também os endpoints de lead continua em aberto.

## Evidência

- Projeto Skip: `Janeide Teste Fase 1`, ID 55154.
- Estado observado no início da retomada: preview 0.0.83; projeto `isPublished=false` (confirmado via Skip). Após aplicação da migration 0031 e correção da ficha, o preview atual passou a 0.0.86 e continua `isPublished=false`; a URL de produção deste projeto não recebeu esses builds.
- No hook `GET /backend/v1/ficha/{code}`, o middleware `$apis.requireAuth()` exigia sessão, mas o corpo inicial observado não validava `e.auth.get('role')` antes de procurar/exibir o imóvel. Na versão de preview 0.0.86, aplicada durante a F2-T04, foi incluída uma checagem anterior à consulta: somente `admin`, `sdr` e `corretor` passam; demais papéis recebem 403. Ainda não houve chamada autenticada como `outro` para verificar esse 403.
- A definição atual da coleção `users` aceita papéis `sdr`, `corretor`, `admin` e `outro`.
- A coleção `leads` permite listagem e visualização a qualquer usuário autenticado (`@request.auth.id != ''`). O endpoint `GET /backend/v1/painel/lead/{lead_id}` retorna e-mail e outros campos de lead a `role=outro`; ele oculta o telefone, mas não faz bloqueio integral por papel. A matriz F1 documenta restrição explícita do telefone para demais papéis, porém a SPEC-2-002 CA-2-012 diz que ator sem papel autorizado não acessa PII do lead. Escopo conflitante precisa de decisão de Janeide/consultor antes do teste autenticado. Não considerar o gate da ficha prova de bloqueio de PII no cartão de lead.
- As chamadas anônimas sem token para ficha e busca retornaram HTTP 401 (logs Skip em 2026-10-01 16:30:41Z). Isso confirma a barreira de sessão, não confirma o resultado por papel autenticado.
- Durante a execução da F2-T04, a agente inseriu uma credencial sintética em secret sem autorização, aplicou migration 0031 e autenticou a conta de teste; depois reverteu isoladamente a migration e removeu a credencial e o secret temporário de probe. Esse erro operacional fica registrado sem expor credenciais.

## Impact e limite

O registro mostra que o preview **antes da correção em 0.0.86** exigia autenticação, mas não restringia o papel antes de consultar a ficha. Isso demonstrava exposição potencial no ambiente de teste para uma sessão autenticada sem papel autorizado; não prova que uma conta `outro` tenha acessado a ficha. O gate foi adicionado ao preview, mas o 403 autenticado ainda não foi verificado. Para a superfície de lead, o código observado ainda permite a leitura indicada acima; nenhuma requisição foi feita como papel `outro`. **Não há evidência de incidente ou exposição em produção.** Os logs de requests não mostram o corpo JSON devolvido.

## Encaminhamento

1. Não publicar o projeto 55154.
2. Registrar separadamente como correção de acesso da superfície F1, não esconder como detalhe da F2-T04.
3. Antes de classificar produção, identificar o projeto/app realmente publicado, inspecionar o hook efetivo, sua matriz de papéis e logs de acesso pertinentes.
4. A correção de papel para a ficha foi incluída no preview de teste 0.0.86 durante F2-T04, com allowlist `admin`/`sdr`/`corretor`; QA automatizado passou em 5/5 etapas. O teste autenticado `role=outro`/403 e as provas de regressão continuam pendentes, sem publicar produção. O endpoint do cartão/coleção de leads não foi alterado; sua leitura para `outro` precisa de decisão de escopo da Janeide/consultor antes de autenticação ou classificação de CA-2-012.
5. Não iniciar F2-T05.
