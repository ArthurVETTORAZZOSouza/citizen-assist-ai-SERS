# Resumo dos testes com usuários (gerado por consolidar_testes.py)

* Participantes: **5** (1 do grupo e 4 externos).
* Compreensão (1 a 5): média **4,6** (5 respostas).
* Utilidade (1 a 5): média **4,8** (5 respostas).
* Tempo para descobrir o gasto do chuveiro (S1): mediana **89 s** (4 sessões com registro automático; sessão `T-JZT3` sem arquivo `.json`).
* Erros de digitação por sessão: média **2,5**; total 10 (nas 4 sessões com JSON).
* Concluíram a S1 sozinhos: 4 de 5.

Atenção: amostra pequena e não aleatória. Os números descrevem estas sessões e não generalizam para a população.
O tempo da S1 é medido automaticamente, da entrada na opção 1 até a exibição do custo mensal.

## Frase para o vídeo e o README
"Testamos com 5 pessoas (1 do grupo e 4 externas). A compreensão média foi 4,6 e a utilidade, 4,8, em escala de 1 a 5; o tempo mediano para descobrir o gasto do chuveiro foi de 89 segundos."

## Comentários recebidos e ajustes (use para preencher CHANGELOG_MELHORIAS.md)
* **T-27J8** (externo, 30-39): S1: Sozinho(a). S2: Sozinho(a). S3: Não consegui. S4: Não testei. Confuso/dúvidas: Na opção de perguntar com as minhas palavras (opção 7), perguntei quanto economizaria mudando a chave do chuveiro de Inverno para Verão, explicando que moro em apartamento alugado e não posso instalar aquecedor solar. O assistente ignorou o "não posso", não respondeu sobre a chave Verão/Inverno e me deu uma explicação sobre como instalar aquecedor solar no telhado do prédio.. Sugestões: Melhoraria a busca da pergunta livre para entender negações (quando o usuário diz que não pode fazer algo) e incluiria informações sobre a economia ao mudar a chave do chuveiro para o modo Verão, além de dicas específicas para quem mora de aluguel e não pode fazer obras, aproveitando os dados do chuveiro que já informei antes.. **Ajuste:** Implementado (Ciclo 1): filtro de negação em responder_texto, tópicos chave_verao_inverno e imovel_alugado e cálculo com o perfil da sessão.
* **T-ALV5** (externo, 50+): S1: Sozinho(a). S2: Sozinho(a). S3: Sozinho(a). S4: Sim. Confuso/dúvidas: Na opção de perguntar com as minhas palavras (opção 7), a resposta principal do assistente apareceu repetida duas vezes seguidas na tela. Além disso, na pergunta sobre o desconto do CadÚnico (Tarifa Social), a resposta foi muito resumida e não explicou os critérios básicos de renda ou o limite de consumo mensal para ter o benefício.. Sugestões: Corrigir a repetição do texto na pergunta livre e detalhar melhor a resposta sobre a Tarifa Social (informando que o benefício vale para famílias inscritas no CadÚnico ou que recebem BPC, com descontos escalonados para consumo de até 220 kWh por mês).. **Ajuste:** Implementado (Ciclo 3): removida duplicidade de mostrar_topico na opcao_pergunta e incluídos critérios da Tarifa Social (CadÚnico/BPC e até 220 kWh/mês).
* **T-JZT3** (grupo, 18-29): S1: Sozinho(a). S2: Sozinho(a). S3: Sozinho(a). S4: Sim. Confuso/dúvidas: -. Sugestões: -. **Ajuste:** Sem ajuste necessário; teste de validação do grupo (18-29) sem problemas relatados (falta arquivo T-JZT3.json na pasta sessoes/).
* **T-NGU8** (externo, 50+): S1: Com ajuda. S2: Com ajuda. S3: Sozinho(a). S4: Não testei. Confuso/dúvidas: Resposta ao usar minhas palavras foi muito generica. Sugestões: Melhorar a visualização das respostas. **Ajuste:** Implementado (Ciclo 2): critérios objetivos de viabilidade do aquecedor solar e simulação automática com o perfil da sessão na opcao_pergunta.
* **T-XLSF** (externo, 18-29): S1: Sozinho(a). S2: Não testei. S3: Não consegui. S4: Não testei. Confuso/dúvidas: Na opção 7, perguntei "Como funciona a Tarifa Social e qual o limite de consumo?" e o sistema respondeu sobre como funciona o aquecedor solar.. Sugestões: tornar a palavra-chave "como funciona" mais específica no tópico de aquecedor solar para não empatar com perguntas sobre Tarifa Social.. **Ajuste:** Pendente de ajuste no código/JSON: em 'Como funciona a Tarifa Social e qual o limite de consumo?', 'como funciona' (13 chars) empatou/venceu 'tarifa social' (13 chars) com ordem anterior; tornar 'como funciona' específico para solar ou desambiguar pontuação.
