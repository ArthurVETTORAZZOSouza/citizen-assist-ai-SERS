# Justificativas das recomendações

Mesma necessidade: **banho quente de uma família de 4 pessoas** na área da Enel SP (região metropolitana de São Paulo). Período de referência comum: **12 meses** e **10 anos**. Todos os números vêm de `calculos/resultados/` e das premissas em `dados/premissas.csv` (as estimadas estão identificadas).

## Resumo comparativo (cenário base)

| Alternativa | Custo/mês | Economia/ano | Investimento | Retorno | Custo total em 10 anos | CO2 evitado/ano |
|---|---|---|---|---|---|---|
| Situação atual (chuveiro elétrico, 12 min) | R$ 133,78 | - | - | - | R$ 16.054 | - |
| A) Uso consciente (8 min) | R$ 89,19 | R$ 535,12 | R$ 0 | imediato | R$ 10.702 | 20,3 kg |
| B) Aquecedor solar (renovável) | R$ 53,51 | R$ 963,22 | R$ 4.500 | 4,7 anos | R$ 10.921 | 36,6 kg |
| A+B) Combinação | R$ 35,67 | R$ 1.177,27 | R$ 4.500 | 3,8 anos | R$ 8.781 | 44,7 kg |

## Premissas do aquecedor solar
* **Coletor de referência (R12):** modelo 1,5 Maxime, classe A do Inmetro, 1,46 m2 e 121,4 kWh/mês nominais. Com o fator de perdas de 0,8 (estimativa do grupo), produz 97,1 kWh/mês, ou 74% da demanda de banho de 132 kWh/mês.
* **Fração solar:** 50% (conservador), 60% (base) e 70% (otimista). Todas ficam abaixo da produção do coletor, e o cenário otimista coincide com a alegação máxima do fabricante (economia de até 70% no aquecimento da água). Nenhum cenário a ultrapassa.
* **Custo:** faixa do Idec (R$ 3.000 a R$ 6.000), a ser substituída por orçamentos reais.

## Custos
* **A) Uso consciente** não exige investimento. Economiza R$ 535,12 por ano para a família de referência e fica ao alcance de qualquer público, inclusive famílias de baixa renda.
* **B) Aquecedor solar** exige investimento inicial (R$ 3.000 a R$ 6.000 segundo o Idec). No cenário base economiza R$ 963,22 por ano e se paga em 4,7 anos; em 10 anos custa R$ 5.132 a menos que a situação atual.
* Cenários do solar: conservador (50% de sol, R$ 6.000) retorna em 7,5 anos; otimista (70% de sol, R$ 3.000), em 2,7 anos.

## Viabilidade
* **A** depende só de hábito. É a recomendação inicial do assistente, por ser imediata e sem custo.
* **B** depende de telhado ou área com sol, do orçamento real, de espaço para o reservatório e, em apartamento, de acordo com o condomínio (Idec). Em dias nublados e no inverno, o apoio elétrico complementa, por isso a economia não é de 100%. Para quem aluga, o investimento pode não compensar.
* A viabilidade do solar **muda com o tamanho da casa**: com 2 moradores o retorno é de 9,3 anos; com 3, 6,2; com 4, 4,7; com 5, 3,7. Por isso o assistente recalcula com os dados do usuário e aceita o orçamento real.

## Impactos ambientais
* O fator médio de emissão da rede brasileira é muito baixo (38,5 kg CO2/MWh em 2023). Por isso o CO2 evitado é **pequeno**: 20,3 kg/ano com o uso consciente e 36,6 kg/ano com o solar. O assistente informa isso com clareza, sem exagerar o benefício ambiental.
* O benefício mais forte do aquecimento solar é a **redução de consumo e de custo**; o Idec também aponta o alívio da demanda no horário de pico. A fabricação, a instalação e o descarte dos equipamentos não foram quantificados.

## Sensibilidade (alternativa B, outras premissas mantidas)
| Variação | Economia/ano | Retorno |
|---|---|---|
| Tarifa R$ 0,80/kWh | R$ 760,32 | 5,9 anos |
| Tarifa R$ 1,20/kWh | R$ 1.140,48 | 3,9 anos |
| Fração solar de 40% | R$ 642,15 | 7,0 anos |
| Fração solar de 90% (acima da alegação do fabricante, apenas para teste) | R$ 1.444,84 | 3,1 anos |

## Recomendações que o assistente faz
1. **Comece pelo banho mais curto** (custo zero, efeito imediato).
2. **Considere o aquecedor solar** se a casa tem 3 ou mais moradores, uso diário do chuveiro e espaço para o sistema; **peça orçamentos** antes de decidir.
3. **Para famílias de baixa renda**, verifique também a Tarifa Social e evite investir sem orçamento fechado.

## Condições e limitações
Todos os valores são estimativas e não garantem economia, geração ou custo. Não foram considerados manutenção, financiamento, instalação extra, variação mês a mês entre verão e inverno, nem mudanças futuras de tarifa. A economia divulgada pelo fabricante é uma alegação do fabricante. O caso-base (simulação da Cemig) supera o consumo do domicílio médio da Enel SP; por isso as respostas do assistente usam os dados informados pelo usuário.
