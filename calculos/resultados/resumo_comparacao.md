# Resumo da comparação de alternativas (gerado por calculos/comparacao_alternativas.py)

Domicílio de referência: 4 moradores, chuveiro de 5500 W, banho de 12 min por pessoa por dia, 30 dias por mês. Tarifa com tributos **estimada**: R$ 1,0135/kWh. Período de referência: 12 meses e 10 anos.

## Cenário base (todas as alternativas para a mesma necessidade)

| Alternativa | kWh/mês | Custo/mês (R$) | Economia/ano (R$) | Investimento (R$) | Retorno (anos) | Custo total em 10 anos (R$) | CO2 evitado (kg/ano) |
|---|---|---|---|---|---|---|---|
| Situação atual (chuveiro elétrico) | 132,0 | 133,78 | 0,00 | 0 | - | 16.054 | 0,0 |
| A) Uso consciente (banho mais curto) | 88,0 | 89,19 | 535,12 | 0 | - | 10.702 | 20,3 |
| B) Aquecedor solar com apoio elétrico | 52,8 | 53,51 | 963,22 | 4.500 | 4,7 | 10.921 | 36,6 |
| A+B) Uso consciente e aquecedor solar | 35,2 | 35,67 | 1.177,27 | 4.500 | 3,8 | 8.781 | 44,7 |

## Aquecedor solar (alternativa B) nos três cenários

| Cenário | Fração solar | Custo do sistema (R$) | Economia/ano (R$) | Retorno (anos) | Custo total em 10 anos (R$) | CO2 evitado (kg/ano) |
|---|---|---|---|---|---|---|
| conservador | 50% | 6.000 | 802,69 | 7,5 | 14.027 | 30,5 |
| base | 60% | 4.500 | 963,22 | 4,7 | 10.921 | 36,6 |
| otimista | 70% | 3.000 | 1.123,76 | 2,7 | 7.816 | 42,7 |

## Verificações de consistência

* Coletor de referência (R12): 1,46 m2 x 83,15 kWh/m2.mês = 121,4 kWh/mês nominais; com fator de perdas de 0,8, **97,1 kWh/mês**, contra uma demanda de 132,0 kWh/mês (74% da demanda). Os cenários de fração solar (50%, 60% e 70%) ficam abaixo dessa produção, e o otimista coincide com a alegação máxima do fabricante (até 70%).
* Simulação da Cemig (R1): reduzir o banho de 12 para 8 min poupa 44,0 kWh/mês; a economia divulgada de R$ 50,54 implica uma tarifa de R$ 1,15/kWh (com tributos, distribuidora de Minas Gerais). A tarifa estimada para a Enel SP (R$ 1,01/kWh) é da mesma ordem de grandeza.
* Retorno: base 4,7 anos e otimista 2,7 anos ficam dentro da faixa de 2 a 7 anos do Idec (R3); o conservador (7,5 anos) fica fora dela e é apresentado como limite inferior.

## Limites

* Não modela a variação entre verão e inverno mês a mês, nem manutenção, financiamento ou custo de instalação extra.
* O cenário-base é um caso de referência (simulação da Cemig); ele supera o consumo do domicílio médio da Enel SP. O assistente recalcula com os dados informados pelo usuário.
* Estimativas de economia, geração e custos não são resultados garantidos.
