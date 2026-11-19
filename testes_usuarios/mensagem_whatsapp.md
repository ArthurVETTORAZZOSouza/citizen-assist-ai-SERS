# Mensagens prontas e formulário (copie e cole)

## Parte 1. Crie o formulário (Google Forms, 5 minutos)
1. Acesse forms.google.com e crie um formulário em branco com o título **"Teste do Citizen Assist AI | Módulo de Energia"**.
2. Descrição: "Obrigado por testar! Não pedimos nome, e-mail nem telefone. As respostas são anônimas e usadas só neste trabalho acadêmico."
3. Em **Configurações**, desligue "Coletar endereços de e-mail" e deixe "Limitar a uma resposta" desligado.
4. Crie as perguntas abaixo, **com estes títulos exatos** (o script `consolidar_testes.py` encontra as colunas por eles):

| # | Título da pergunta | Tipo | Opções |
|---|---|---|---|
| 1 | Código da sessão (aparece no final do teste, ex.: T-7K2Q) | Resposta curta (obrigatória) | |
| 2 | Você faz parte do grupo do projeto? | Múltipla escolha | Sim, sou do grupo / Não, sou externo |
| 3 | Faixa etária | Múltipla escolha | 18-29 / 30-39 / 40-49 / 50+ |
| 4 | S1. Consegui descobrir quanto o meu chuveiro gasta por mês | Múltipla escolha | Sozinho(a) / Com ajuda / Não consegui / Não testei |
| 5 | S2. Consegui comparar o aquecedor solar com o banho mais curto | Múltipla escolha | Sozinho(a) / Com ajuda / Não consegui / Não testei |
| 6 | S3. Consegui perguntar com as minhas palavras e recebi uma resposta útil | Múltipla escolha | Sozinho(a) / Com ajuda / Não consegui / Não testei |
| 7 | S4. Quando digitei algo inválido, a mensagem me ajudou | Múltipla escolha | Sim / Mais ou menos / Não / Não testei |
| 8 | Entendi o que o assistente me disse. | Escala linear de 1 a 5 (1 = discordo totalmente, 5 = concordo totalmente) | |
| 9 | As orientações me ajudariam a decidir como economizar. | Escala linear de 1 a 5 | |
| 10 | O que foi confuso? Quais dúvidas você teve? | Parágrafo | |
| 11 | Sugestões: o que você mudaria? | Parágrafo | |

5. Clique em **Enviar**, copie o link e use nas mensagens abaixo.

## Parte 2. Mensagem para quem vai rodar no próprio computador (Brayan e Giovanne)
> Oi! Preciso que você teste o protótipo do meu trabalho de Energias (ele calcula quanto o chuveiro gasta e compara com aquecedor solar). Leva uns 10 minutos.
> 1) Baixe e extraia a pasta que mandei (citizen-assist-ai-energia).
> 2) Abra o terminal dentro dessa pasta e rode: `python assistente/assistente.py --teste`  (precisa do Python 3.9 ou superior; confira com `python --version`).
> 3) Use o assistente sem pedir ajuda. Tente: (S1) descobrir quanto o seu chuveiro gasta por mês; (S2) ver se vale a pena trocar por aquecedor solar; (S3) perguntar com as suas palavras como economizar no banho; (S4) digitar algo sem sentido (letras onde pede número) para ver a mensagem de erro.
> 4) No final aparece um **código de sessão (T-XXXX)** e o caminho de um arquivo. **Me mande esse arquivo por aqui.**
> 5) Responda o formulário (leva 3 minutos), informando o código: LINK_DO_FORMULARIO
> Anote as dúvidas que tiver durante o teste e coloque no formulário. Obrigado!

## Parte 3. Mensagem para quem vai testar com você, em pessoa (seus pais)
Antes: abra o terminal no seu computador, na pasta do projeto, e rode `python assistente/assistente.py --teste`. Entregue o computador, **sem explicar como usar**. Leia o texto da `ficha_sessao.md` ("É um protótipo... o teste avalia o assistente, não você") e peça as situações S1 a S4 uma de cada vez.
Depois, envie o link do formulário pelo WhatsApp para a pessoa responder no celular, ou leia as perguntas e marque por ela, e **informe o código da sessão** que aparece no final.
Se for à distância, use chamada de vídeo com compartilhamento de tela, e registre na pergunta 10 que o teste foi "assistido".

## Parte 4. Depois dos testes
1. Coloque os arquivos `T-XXXX.json` recebidos na pasta `testes_usuarios/sessoes/`.
2. No formulário, vá em **Respostas > Ver no Planilhas > Arquivo > Fazer download > .csv** e salve como `testes_usuarios/respostas_forms.csv`.
3. Rode `python testes_usuarios/consolidar_testes.py`. Ele cria `registro_testes.csv` (com tempos, erros e respostas já unidos) e `resumo_testes.md` (médias, frase pronta para o vídeo e lista de comentários).
4. Preencha à mão apenas o `ajustes_realizados.md` e a coluna `ajuste_gerado`.

## Plano B, sem formulário
Se não der para criar o formulário, peça que a pessoa responda no WhatsApp neste modelo, e você digita as respostas no `registro_testes.csv` seguindo a `ficha_sessao.md`:
```
Código da sessão: T-XXXX
Grupo ou externo:
Faixa etária (18-29 / 30-39 / 40-49 / 50+):
S1 (sozinho / com ajuda / não consegui / não testei):
S2:
S3:
S4 (sim / mais ou menos / não / não testei):
Entendi o que o assistente disse (1 a 5):
As orientações ajudariam a decidir como economizar (1 a 5):
O que foi confuso? Dúvidas:
Sugestões:
```
