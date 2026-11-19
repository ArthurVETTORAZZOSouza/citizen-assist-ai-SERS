# Ficha de sessão (use uma por participante; pode ser impressa ou preenchida no celular)

## Identificação (sem nome e sem dados pessoais)
* Código: T__ (T01, T02, ...)
* Data: __/__/2026
* **Grupo ou externo:** grupo / externo
* Faixa etária: 18-29 / 30-39 / 40-49 / 50+
* Quem observou: __________

## Antes de começar (leia em voz alta)
"É um protótipo educacional. As respostas são estimativas. Você pode parar quando quiser. Não vou ajudar durante o uso, só observar. O teste avalia o assistente, não você."

## Situações (anote o que aconteceu, em poucas palavras)
| Situação | Concluiu? (sozinho / com ajuda / não) | Erros de entrada (quantas vezes apareceu "Não entendi" ou "fora do esperado") | Dúvida ou comentário dito em voz alta |
|---|---|---|---|
| S1. "Descubra quanto o seu chuveiro gasta por mês." **Cronometre: do pedido até a pessoa ler o custo mensal.** Tempo: ____ s | | | |
| S2. "Veja se vale a pena trocar por aquecedor solar." | | | |
| S3. "Pergunte, com as suas palavras, como economizar no banho." | | | |
| S4. "Digite algo que não faça sentido (letras onde pede número)." | | | |

Regra de ajuda: se a pessoa ficar travada por mais de 3 minutos, diga "pode apertar ENTER para usar o valor sugerido" e anote **"com ajuda"** e o motivo (por exemplo, "não sabia a potência do chuveiro").

## Perguntas finais
1. "Entendi o que o assistente me disse." Nota de 1 a 5: ____ (1 = discordo totalmente, 5 = concordo totalmente)
2. "As orientações me ajudariam a decidir como economizar." Nota de 1 a 5: ____
3. O que foi confuso? ______________________
4. O que você mudaria? ______________________

## Como transformar esta ficha em UMA linha do `registro_testes.csv`
Cabeçalho do arquivo: `codigo,data,grupo_ou_externo,faixa_etaria,situacoes_testadas,compreensao_1a5,utilidade_1a5,tempo_s1_segundos,erros_de_entrada,comentarios,ajuste_gerado`

Modelo (troque cada trecho entre `<>` pelo que de fato aconteceu; não copie valores de exemplo):
```
<T01>,<dd/mm/aaaa>,<grupo ou externo>,<faixa>,"S1;S2;S3;S4",<nota 1 a 5>,<nota 1 a 5>,<segundos da S1>,<total de erros nas 4 situações>,"S1: <resumo>. S2: <resumo>. S3: <resumo>. S4: <resumo>. Confuso: <resposta>. Mudaria: <resposta>.",<deixe vazio até decidir o ajuste>
```
Dicas:
* Mantenha os comentários entre aspas. Isso evita problemas com vírgulas.
* Se abrir o arquivo no Excel e as colunas ficarem juntas, edite o arquivo como texto no PyCharm.
* Se uma situação não foi testada, escreva "não testada" nos comentários e tire-a de `situacoes_testadas`.
* Guarde esta ficha (papel ou foto da anotação **sem identificar a pessoa**) até a entrega, para o caso de o professor pedir.

## Depois dos testes: o que fazer com as sugestões
Nem toda sugestão precisa virar mudança. Em `CHANGELOG_MELHORIAS.md`, registre **todas** com um destes status:
* **Implementado:** descreva a mudança (arquivo ou commit).
* **Não implementado:** explique o motivo (fora do escopo, não cabe no prazo, contraria uma fonte) e marque como **melhoria futura**.

Priorize o que (1) impediu alguém de entender ou concluir S1 ou S2 e (2) dá para corrigir em até 30 minutos.
