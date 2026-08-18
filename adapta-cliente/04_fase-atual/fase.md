# Fase 1 — Tarefas gerais

**Objetivo:** organizar a entrada de leads, o atendimento inicial, a consulta de imóveis e o pedido de visita.

**Regra de execução:** usar somente ambiente de teste; executar uma task por vez; se uma informação,
acesso ou permissão não estiver definido, parar e registrar a pendência.

## Tasks

| ID | Leva | Task | Responsável | Fazer | Concluída quando | Evidência | Depende de | Pare se | Status |
|---|---:|---|---|---|---|---|---|---|---|
| F1-T01 | 1 | Definir como um novo contato entra | Matheus Silva | Definir canal, origem, sistema, informações mínimas, permissões e regra para não repetir o contato. | Fontes, campos, acessos e responsáveis aprovados. | Decisão registrada e exemplo de lead de teste. | Call de setup | WhatsApp, CRM, acesso ou regra de repetição não definidos. | PENDENTE |
| F1-T02 | 1 | Definir a tela de atendimento do lead | Matheus Silva | Definir onde o SDR verá os leads, quais dados aparecerão e o que cada papel poderá fazer. | Tela, campos e permissões aprovados. | Desenho da tela e regras de acesso. | Call de setup | Campo pessoal ou acesso sem responsável. | PENDENTE |
| F1-T03 | 1 | Definir de onde vêm os dados dos imóveis | Matheus Silva | Escolher a fonte oficial, dados obrigatórios, situação do imóvel, preço, taxas, fotos, validade e responsável pela atualização. | Uma fonte e um imóvel de teste definidos. | Decisão da fonte e ficha de exemplo. | Call de setup | As fontes apresentarem informações diferentes. | PENDENTE |
| F1-T04 | 1 | Definir como registrar pedido de visita sem marcar horário | Janeide Xavier | Definir informações mínimas, preferência de data, horário, fuso, responsável e próximo passo. | O pedido puder ficar como `Pendente de agenda`, sem reserva. | Exemplo de pedido preenchido. | Call de setup | Alguém solicitar reserva, corretor ou horário nesta fase. | PENDENTE |
| F1-T05 | 2 | Testar a entrada de um lead pelo link | Matheus Silva | Usar um link aprovado e um contato fictício para criar um lead com origem e imóvel de interesse. | Um lead aparecer uma única vez com as informações corretas. | ID do lead e captura de tela. | F1-T01 | Não houver ambiente de teste, acesso ou identificação da entrada. | BLOQUEADA |
| F1-T06 | 3 | Colocar o lead na fila de atendimento | Matheus Silva | Fazer o lead aparecer na fila com origem, situação, imóvel e próximo passo. | O SDR encontrar o lead e registrar o próximo passo. | Captura do cartão e registro da alteração. | F1-T02 e F1-T05 | O cartão estiver duplicado, incompleto ou mostrar dado não autorizado. | BLOQUEADA |
| F1-T07 | 4 | Consultar um imóvel e mostrar sua ficha | Matheus Silva | Consultar um código de teste e abrir a ficha para conferência do SDR. | A ficha mostrar somente informações confirmadas, fonte e validade. | Captura da ficha e identificação da fonte. | F1-T03 e F1-T06 | O imóvel estiver vencido, incompleto ou com foto/link não confiável. | BLOQUEADA |
| F1-T08 | 5 | Registrar interesse em visita sem reservar horário | SDR | Registrar o pedido ligado ao lead e ao imóvel, com preferência de data e próximo passo. | O pedido aparecer como `Pendente de agenda`. | ID do pedido e captura do cartão. | F1-T04, F1-T06 e F1-T07 | O sistema tentar criar horário, corretor, chave ou reserva. | BLOQUEADA |
| F1-T09 | 6 | Testar problemas na entrada de leads | Matheus Silva | Testar código inválido, entrada repetida, pedido para não receber contato e sistema indisponível. | Cada situação gerar o bloqueio ou a pendência correta, sem duplicar lead. | Relatório dos quatro testes. | F1-T05 | Houver lead duplicado, envio indevido ou informação pessoal exposta. | BLOQUEADA |
| F1-T10 | 6 | Testar acessos e dados incompletos no atendimento | Matheus Silva | Testar usuário sem permissão, lead incompleto e painel indisponível. | O acesso indevido for bloqueado e a pendência puder ser recuperada. | Registros de acesso, pendência e recuperação. | F1-T06 | Alguém conseguir alterar ou ver informação sem autorização. | BLOQUEADA |
| F1-T11 | 6 | Testar imóveis que não podem ser enviados | Matheus Silva | Testar imóvel inativo, dados faltantes, informações diferentes, foto/link inseguro e reenvio. | O envio incorreto for bloqueado com o motivo explicado. | Relatório dos testes e registros dos bloqueios. | F1-T07 | Dado não confirmado for enviado ao cliente. | BLOQUEADA |
| F1-T12 | 6 | Testar pedidos de visita incompletos ou repetidos | SDR | Testar pedido sem horário definido, pedido repetido e tentativa de marcar horário. | O pedido incompleto pedir esclarecimento, a repetição não criar outro registro e a reserva ser bloqueada. | Pedido, registro da repetição e bloqueio da reserva. | F1-T08 | Qualquer pedido for tratado como visita marcada. | BLOQUEADA |
| F1-T13 | 7 | Demonstrar a entrada completa de um lead | SDR | Demonstrar o caminho do link até o lead pronto para atendimento. | Os quatro critérios da entrada forem aprovados. | Vídeo ou capturas, registros e aceite do SDR/Matheus. | F1-T09 | Qualquer cenário de entrada falhar. | BLOQUEADA |
| F1-T14 | 7 | Demonstrar fila, próximo passo e histórico do lead | SDR | Abrir a fila, localizar o lead, registrar o próximo passo e consultar o histórico. | O atendimento continuar sem perder origem ou histórico. | Captura da fila, registro do próximo passo e histórico. | F1-T10 | Houver vazamento de dados ou alteração indevida. | BLOQUEADA |
| F1-T15 | 7 | Demonstrar ficha correta e envio pelo SDR | SDR | Consultar o imóvel, revisar a ficha e confirmar o envio manual. | O envio ficar ligado ao lead, imóvel, usuário e horário, sem repetição. | Ficha, confirmação de envio e registro do vínculo. | F1-T11 | Houver dado inventado, vencido ou envio repetido. | BLOQUEADA |
| F1-T16 | 7 | Demonstrar pedido de visita pendente | SDR | Registrar o pedido, mostrar o próximo passo e demonstrar que nenhum horário foi reservado. | O pedido estiver pronto para ser tratado na Fase 3. | Pedido, situação, bloqueio de reserva e aceite. | F1-T12 | O sistema criar reserva, horário ou corretor automaticamente. | BLOQUEADA |

## Ordem de execução

- F1-T01 a F1-T04 são as definições iniciais e são independentes entre si.
- F1-T05 a F1-T08 formam o caminho principal e devem seguir as dependências indicadas.
- F1-T09 a F1-T12 testam problemas depois que o caminho principal correspondente estiver pronto.
- F1-T13 a F1-T16 são as demonstrações finais da Fase 1.
