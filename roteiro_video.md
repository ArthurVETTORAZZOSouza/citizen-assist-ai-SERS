# Roteiro do vídeo técnico (máximo 3 minutos, YouTube não listado)

Sugestão de divisão: três vozes (Arthur, Brayan, Giovanne). Cerca de 350 palavras, ritmo calmo. Ensaie cronometrando: o limite é de 3 minutos.
Antes de gravar, rode `python assistente/assistente.py` e deixe o terminal com fonte grande.

| Tempo | Quem | Tela | Fala sugerida |
|---|---|---|---|
| 0:00 a 0:25 | Arthur | Título e imagem de uma família | "Pense em uma família de quatro pessoas na região metropolitana de São Paulo. Todo dia, quatro banhos quentes. No chuveiro elétrico, esse banho é uma das maiores parcelas da conta de luz. Nosso público são os responsáveis pela conta de luz das famílias atendidas pela Enel SP, inclusive de idosos e de baixa renda, que precisam entender a conta e decidir como economizar. O módulo de energia do Citizen Assist AI responde a essa necessidade." |
| 0:25 a 1:10 | Brayan | `calculos/resultados/resumo_comparacao.md` e a tabela de premissas | "Energia é potência vezes tempo. Um chuveiro de 5.500 watts, 12 minutos por pessoa, 4 pessoas, 30 dias: 132 quilowatts-hora por mês. Com o preço estimado de R$ 1,01 por kWh, são cerca de R$ 134 por mês. Usamos dados reais da base SAMP da ANEEL para a Enel SP e fontes como Cemig, Idec, Inmetro e MCTI. O que é estimativa está marcado como estimativa." |
| 1:10 a 2:00 | Giovanne | `grafico_custo_anual.png` e `grafico_custo_acumulado.png` | "Comparamos duas alternativas para a mesma necessidade, em 12 meses e em 10 anos. A, banho de 8 minutos: custo zero e economia de cerca de R$ 535 por ano. B, aquecedor solar, a fonte renovável: com um coletor real de classe A do Inmetro, sistema de R$ 4.500 no cenário base, economia de cerca de R$ 963 por ano e retorno em 4,7 anos. No cenário conservador o retorno sobe para 7,5 anos, no otimista cai para 2,7. Em CO2 o ganho é pequeno, cerca de 37 quilos por ano, porque a rede brasileira já é limpa. O valor está no bolso." |
| 2:00 a 2:40 | Arthur | Terminal com o assistente | "Agora, o assistente. Na opção 1 informo potência, minutos, pessoas e o preço do kWh da conta. Se eu digito uma letra, ele pede um número. Na opção 2 ele compara as alternativas, aceita o orçamento real do aquecedor, mostra três cenários, avisa que é estimativa e cita as fontes. Também respondo perguntas com as próprias palavras, como: aquecedor solar compensa?" |
| 2:40 a 3:00 | Os três | Slide final com as recomendações | "Recomendação: comece pelo banho mais curto. Considere o aquecedor solar em casas com três ou mais moradores, e peça orçamentos. Limitações: são estimativas, não garantias; não incluímos manutenção nem a variação entre verão e inverno. Testamos em 3 sessões reais e ajustamos o filtro de negação na busca livre, a resposta duplicada na opção 7 e o detalhamento da Tarifa Social e do aquecedor solar." |

## Checklist antes de publicar
* Duração máxima de 3 minutos (confira no YouTube após o envio).
* Publicar como **não listado** e testar o link em uma janela anônima.
* Mostrar: público e necessidade, análise de consumo, comparação com a fonte renovável, demonstração do assistente, recomendações e limitações.
* Substituir os trechos entre colchetes pelos resultados **reais** dos testes com usuários.
