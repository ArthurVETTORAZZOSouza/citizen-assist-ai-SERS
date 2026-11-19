# Registro de Evolução e Melhorias — Citizen Assist AI (Energia)

Este documento registra as melhorias implementadas no protótipo a partir dos testes de usabilidade realizados com usuários reais, detalhando o problema encontrado, a solução técnica aplicada e o resultado esperado.

---

## Ciclo 1 — Teste com Usuário: T-27J8 (Perfil: Morador de Imóvel Alugado)

### 1. Cenário e Problema Identificado
* **Contexto do teste:** Na **Opção 7 (Perguntar com as minhas palavras)**, o usuário informou que mora em apartamento alugado, não pode instalar aquecedor solar e perguntou quanto economizaria mudando a chave do chuveiro de 5.500 W da posição *Inverno* para *Verão*.
* **Falha observada:** O motor de busca (`responder_texto`) pontuava apenas o tamanho das palavras-chave encontradas (`len(k)`). Termos longos como `"aquecedor solar"` e `"apartamento"` dominaram a pontuação, fazendo o assistente ignorar a negação (*"não posso instalar"*) e devolver instruções sobre instalação de coletores solares no telhado.
* **Lacuna de conteúdo:** A base de conhecimento não possuía orientações sobre a chave seletora (*Verão/Inverno*) nem recomendações exclusivas sem obras para inquilinos.

### 2. Melhorias Implementadas
* **Tratamento de negação na busca (`assistente.py`):** Adicionado pré-processamento com expressão regular (`re.sub`) na função `responder_texto` para filtrar trechos precedidos por termos negativos (`"nao"`, `"sem"`, `"dispenso"`, `"nunca"`), evitando falsos positivos.
* **Expansão da base de conhecimento (`base_conhecimento.json`):**
  * Criação do tópico `chave_verao_inverno` explicando a redução de 30% a 40% no consumo elétrico ao mudar a chave seletora, embasado em orientações da ANEEL/Procel (`R13`).
  * Criação do tópico `imovel_alugado` com medidas de custo zero para moradores que não podem realizar reformas.
  * Remoção de ambiguidade na palavra-chave `"inverno"` do tópico `solar_como`.
* **Personalização com memória de sessão (`assistente.py`):** Atualização da `opcao_pergunta` para cruzar a dúvida sobre a chave seletora com os dados já informados pelo usuário na sessão (`perfil`), exibindo a economia estimada em reais por mês.

### 3. Resultado Esperado (Pós-Melhoria)
Ao repetir a mesma pergunta com contexto de negação e restrição de aluguel, o assistente identifica corretamente a intenção sobre a chave seletora, orienta medidas sem obra e calcula o impacto financeiro personalizado para o chuveiro do usuário.

---

## Ciclo 2 — Teste com Usuário: T-NGU8 (Perfil: Avaliação de Viabilidade do Aquecedor Solar)

### 1. Cenário e Problema Identificado
* **Contexto do teste:** Na **Opção 7 (Perguntar com as minhas palavras)**, o usuário perguntou: *"Quando vale a pena usar o aquecedor solar?"*.
* **Feedback do usuário:** A resposta foi considerada **muito genérica**, pois apresentava apenas valores médios de mercado (R$ 3.000 a R$ 6.000) e prazo amplo de retorno (2 a 7 anos), sem esclarecer quais características práticas do imóvel ou da família tornam o investimento vantajoso.

### 2. Melhorias Implementadas
* **Critérios objetivos de decisão (`base_conhecimento.json`):** Reescrita da resposta do tópico `solar_custo` para destacar os três fatores decisivos de viabilidade (número de moradores/consumo alto, propriedade do imóvel com acesso ao telhado e incidência solar).
* **Simulação automática com contexto (`assistente.py`):** Inclusão de cálculo dinâmico na `opcao_pergunta` para que, caso o usuário já tenha informado os dados do banho na sessão, o assistente exiba imediatamente a economia anual e o tempo de retorno (*payback*) estimados para a realidade dele.
* **Atualização do roteiro de demonstração (`assistente.py`):** Inclusão das perguntas dos Ciclos 1 e 2 na função `demo()` para validação automatizada.

### 3. Resultado Esperado (Pós-Melhoria)
Ao perguntar quando o aquecedor solar compensa, o usuário recebe tanto os critérios práticos para avaliar o seu imóvel quanto uma estimativa personalizada baseada no seu próprio perfil de consumo.

---
## Ciclo 3 — Teste com Usuário: T-ALV5 (Perfil: Beneficiária CadÚnico e Validação de Erros)

### 1. Cenário e Problemas Identificados
* **Contexto do teste:** A usuária testou a **Opção 1** inserindo uma entrada com unidade de medida (`"4600W"`), utilizou a **Opção 2** com tarifa social reduzida (`R$ 0,65/kWh`) e realizou consultas livres na **Opção 7** sobre desconto pelo CadÚnico e viabilidade de aquecedor solar.
* **Comportamentos observados:**
  * **Validação de entrada (Ponto positivo):** A mensagem de erro orientou claramente o preenchimento apenas numérico, permitindo à usuária corrigir o dado sozinha.
  * **Bug de interface (`assistente.py`):** Na **Opção 7**, a chamada `mostrar_topico(topico)` foi executada duas vezes seguidas, duplicando o texto da resposta e as fontes na tela.
  * **Resposta superficial (`base_conhecimento.json`):** Ao perguntar sobre desconto na conta de luz com CadÚnico, o tópico `baixa_renda` devolveu uma resposta genérica sem explicar os critérios de renda, BPC ou o limite de consumo de 220 kWh.

### 2. Melhorias Implementadas
* **Correção de duplicidade na exibição (`assistente.py`):** Remoção da chamada redundante de `mostrar_topico(topico)` dentro da função `opcao_pergunta`.
* **Enriquecimento do tópico `baixa_renda` (`base_conhecimento.json`):** Inclusão dos critérios objetivos da Tarifa Social de Energia Elétrica (CadÚnico, BPC, faixas de desconto de 10% a 65% até 220 kWh/mês e orientação para conferência na fatura), mantendo a referência `R11`.

### 3. Resultado Esperado (Pós-Melhoria)
As respostas da **Opção 7** passam a ser exibidas uma única vez de forma limpa, e usuários que buscam informações sobre benefícios sociais recebem os critérios exatos para verificar seu direito na conta de luz.


---

## Ciclo 4 — Teste com Usuário: T-XLSF (Perfil: Dúvida sobre Tarifa Social e Limite de Consumo)

### 1. Cenário e Problema Identificado
* **Contexto do teste:** Na **Opção 7 (Perguntar com as minhas palavras)**, o participante (externo, faixa 18–29) perguntou: *"Como funciona a Tarifa Social e qual o limite de consumo?"*.
* **Falha observada:** O motor de busca (`responder_texto`) pontua os tópicos pela soma do comprimento das palavras-chave encontradas (`len(k)`) e mantém o primeiro tópico em caso de empate (`p > pontos`). Como a expressão genérica `"como funciona"` estava cadastrada no tópico `solar_como` (que aparece antes de `baixa_renda` na base) e empatava em pontuação com `"tarifa social"`, o assistente respondeu sobre o funcionamento do aquecedor solar em vez da Tarifa Social.

### 2. Melhorias Implementadas
* **Desambiguação de palavras-chave (`base_conhecimento.json`):**
  * Substituição da palavra-chave genérica `"como funciona"` por `"como funciona o aquecedor"` no tópico `solar_como`, restringindo o termo ao contexto do aquecimento solar.
  * Inclusão das palavras-chave `"limite de consumo"` e `"220 kwh"` no tópico `baixa_renda` para reforçar a correspondência em perguntas sobre regras e faixas da Tarifa Social.

### 3. Resultado Esperado (Pós-Melhoria)
Ao repetir a pergunta *"Como funciona a Tarifa Social e qual o limite de consumo?"*, não há mais conflito com `solar_como`: o assistente identifica corretamente o tópico `baixa_renda` e apresenta os critérios do CadÚnico/BPC e o limite mensal de 220 kWh.
