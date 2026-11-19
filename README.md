# Citizen Assist AI | Módulo de Energia

**Global Solution | Soluções em Energias Renováveis e Sustentáveis**
Contribuição da disciplina de Soluções em Energias Renováveis e Sustentáveis ao desafio Citizen Assist AI (CitizenTech).

## Integrantes
| Nome | RM |
|---|---|
| Arthur Vettorazzo de Souza | 569445 |
| Brayan Barbosa Dos Santos | 573682 |
| Giovanne Gomes Petenuci | 574091 |

> Este repositório é dedicado à disciplina de Energias Renováveis e Sustentáveis. Caso seja integrado a um repositório compartilhado com outras disciplinas, esta pasta e o módulo `assistente/` identificam a contribuição de energia.

## 1. Público e problema
**Público:** responsáveis pela conta de luz de famílias da região metropolitana de São Paulo atendidas pela Enel SP, incluindo familiares de idosos e famílias de baixa renda, que usam chuveiro elétrico. O protótipo desta entrega é em texto (terminal). Como o desafio Citizen Assist AI prevê perfis de acessibilidade (por exemplo, guiado e por voz), as mesmas respostas podem ser entregues por esses perfis por meio de `assistente/modulo_energia.py`, descrito na seção 2.1.
**Necessidade energética:** entender quanto o banho quente pesa na conta de luz e decidir como reduzir esse gasto, comparando alternativas de economia e uma fonte renovável (aquecimento solar de água).
**Como as orientações contribuem:** o assistente transforma potência, tempo de banho e tarifa em um custo mensal claro, compara alternativas para a mesma necessidade e indica fontes e limitações.

## 2. Funcionalidades de energia (`assistente/`)
Assistente de terminal em Python (apenas biblioteca padrão), com menu numerado e perguntas em texto livre.

| Opção | O que faz |
|---|---|
| 1 | Calcula energia (kWh) e custo (R$) do chuveiro com os dados informados |
| 2 | Compara situação atual, **A) uso consciente**, **B) aquecedor solar** e **A+B**, com 3 cenários; aceita o **orçamento real** do usuário e avisa quando a estimativa foi pensada para 4 moradores |
| 3 e 4 | Dicas de economia e informações sobre aquecedor solar (custo, retorno, limites) |
| 5 | Dados reais da Enel SP em 2025 (base SAMP da ANEEL) |
| 6 | Fontes e limitações |
| 7 | Pergunta livre, entendida por palavras-chave; fora do escopo, o assistente avisa |

**Segurança e acessibilidade básica:** linguagem simples, valores sugeridos com ENTER, comando `voltar` em qualquer pergunta, validação de entradas inválidas (letras, negativos, valores fora da faixa, vírgula decimal), nenhum dado pessoal coletado, aviso de que não é canal oficial e de que os números são estimativas.

### 2.1 Integração ao Citizen Assist AI
O módulo é exposto como funções puras (sem `input()` nem `print()`) em [`assistente/modulo_energia.py`](assistente/modulo_energia.py), para ser usado por outro assistente, interface ou disciplina do projeto:

```python
import sys; sys.path.insert(0, "assistente")
from modulo_energia import responder_energia, calcular_banho, comparar_banho

r = responder_energia("aquecedor solar compensa?")   # texto, referências e aviso de estimativa
c = calcular_banho(5500, 12, 4, tarifa=1.01)          # kWh/mês e custo
d = comparar_banho(5500, 12, 8, 4, 1.01, orcamento=4500)  # alternativas e três cenários solares
```
Todas as respostas trazem as referências e o aviso de que os números são estimativas. O assistente de terminal (`assistente.py`) usa a mesma base de conhecimento e os mesmos cálculos.

## 3. Como executar e testar
Requer Python 3.9 ou superior. Execute os comandos dentro da pasta que contém este `README.md`.
```bash
python assistente/assistente.py            # modo interativo
python assistente/assistente.py --demo     # demonstração roteirizada (inclui entradas inválidas)
python calculos/comparacao_alternativas.py # recalcula a comparação, os CSVs e os gráficos
python -m unittest discover -s testes -v   # testes automáticos (33 testes)
```
Os gráficos e o reprocessamento da base SAMP usam `matplotlib` e `pandas` (`pip install -r requirements.txt`).

## 4. Estrutura
```
assistente/            assistente.py (terminal), modulo_energia.py (integração) e base_conhecimento.json
calculos/              energia.py (funções), comparacao_alternativas.py e resultados/ (CSVs, resumo e gráficos)
dados/                 premissas.csv, samp_enel_sp_2025.csv, base intermediária e scripts de preparação
docs/                  fontes.md, justificativas_recomendacoes.md, roteiro_video.md
testes/                testes automáticos
testes_usuarios/       roteiro, ficha, formulário, sessões, consolidar_testes.py, registro e ajustes
entrega.txt            arquivo de entrega do Portal
```

## 5. Dados utilizados, origem e premissas
Todas as premissas estão em [`dados/premissas.csv`](dados/premissas.csv), com **valor, unidade, tipo (dado oficial, dado de fabricante, dado de fatura, referência ou estimado) e fonte**. Os cálculos leem esse arquivo, que é a única fonte de verdade.

**Dados reais (ANEEL, base SAMP, 2025, classe Residencial, mercado Regular, Enel SP):** consumo médio de 189,9 kWh/mês por consumidor (todos os usos da casa); cerca de 17,8% de consumidores de baixa renda; tarifa média sem tributos de R$ 0,61/kWh (jan a jun) e R$ 0,73/kWh (jul a dez). Preparação em `dados/prep_base.py` e `dados/extrair_enel_sp.py`. Unidades: kWh, R$ e R$/kWh; período: janeiro a dezembro de 2025.

**Dados de fabricante:** coletor solar de referência (Komeco, modelo 1,5 Maxime, classe A do Inmetro): 1,46 m2 e 121,4 kWh/mês (R12).

**Dados estimados (identificados como tais):** tarifa com tributos (R$ 1,01/kWh = (TUSD + TE com tributos nas faturas B1) x 1,0902 do reajuste de 2026), custo do aquecedor solar (R$ 3.000 a R$ 6.000, faixa do Idec), fração de energia atendida pelo sol (50%, 60% e 70%) e fator de perdas do sistema (0,8).

## 6. Cálculos e comparação das alternativas
**Conceitos aplicados:** potência (kW) é energia por unidade de tempo; energia (kWh) = potência (kW) x tempo (h); custo (R$) = kWh x tarifa; o chuveiro elétrico é uma resistência com rendimento próximo de 100%; o aquecedor solar transfere calor do sol para a água e a rede só complementa; emissões evitadas = kWh evitados x fator de emissão da rede.

**Caso de referência:** 4 moradores, chuveiro de 5.500 W, 12 minutos por pessoa por dia, 30 dias (simulação da Cemig, R1). Energia: 5,5 kW x 0,2 h x 4 x 30 = 132 kWh/mês. **Mesma necessidade, período comum de 12 meses e 10 anos.**

| Alternativa | Custo/mês | Economia/ano | Investimento | Retorno | Custo total em 10 anos | CO2 evitado/ano |
|---|---|---|---|---|---|---|
| Situação atual | R$ 133,78 | - | - | - | R$ 16.054 | - |
| A) Uso consciente (8 min) | R$ 89,19 | R$ 535,12 | R$ 0 | imediato | R$ 10.702 | 20,3 kg |
| B) Aquecedor solar (renovável) | R$ 53,51 | R$ 963,22 | R$ 4.500 | 4,7 anos | R$ 10.921 | 36,6 kg |
| A+B | R$ 35,67 | R$ 1.177,27 | R$ 4.500 | 3,8 anos | R$ 8.781 | 44,7 kg |

Cenários do aquecedor solar: conservador (50% de sol, R$ 6.000) retorno de 7,5 anos; base (60%, R$ 4.500), 4,7 anos; otimista (70%, R$ 3.000), 2,7 anos. Verificações de consistência e análises de sensibilidade (tarifa, número de moradores e fração solar) estão em `calculos/resultados/`.

**Verificação cruzada (fórmula):** o exemplo numérico do Idec (R3), chuveiro de 5.500 W por 1 hora por dia durante 30 dias, dá 165 kWh e R$ 122,10 a R$ 0,74/kWh; a função `energia_kwh_mes()` reproduz esse resultado (teste automático em `testes/test_calculos.py`).

**Verificação cruzada (caso-base):** a simulação da Cemig (12 para 8 min = 44 kWh/mês, R$ 50,54) implica R$ 1,15/kWh em Minas Gerais, da mesma ordem da tarifa estimada para a Enel SP.

**Verificação cruzada (solar):** o coletor de referência (R12) produz 121,4 kWh/mês nominais; com o fator de perdas de 0,8, 97,1 kWh/mês, ou 74% da demanda de banho. Os cenários de 50%, 60% e 70% ficam abaixo disso, e o otimista coincide com a alegação máxima do fabricante (economia de até 70%), que é uma alegação do fabricante e não um resultado garantido.

## 7. Justificativas das recomendações
Detalhadas em [`docs/justificativas_recomendacoes.md`](docs/justificativas_recomendacoes.md), considerando **custos, viabilidade e impactos ambientais**. Em resumo: começar pelo banho mais curto (custo zero); considerar o aquecedor solar em casas com 3 ou mais moradores e pedir orçamentos; o ganho de CO2 é pequeno porque a rede elétrica brasileira já é limpa, então o argumento principal do solar é financeiro.

## 8. Como a análise sustenta o assistente
| Resposta do assistente | Origem na análise |
|---|---|
| Custo do chuveiro (opção 1) | `calculos/energia.py`: energia e custo, com as premissas de `dados/premissas.csv` |
| Comparação e recomendação (opção 2) | `comparar_alternativas()` e `cenarios_solares()` (os mesmos usados em `calculos/comparacao_alternativas.py`) |
| Dados da Enel SP (opção 5) | `dados/samp_enel_sp_2025.csv` (base SAMP da ANEEL) |
| Custos, retorno e emissões nas respostas livres | `assistente/base_conhecimento.json`, com as referências R1 a R12 |
| Avisos e limitações | Texto fixo `AVISO` em todas as respostas com números |

## 9. Referências
Lista completa, com o que cada fonte sustenta, em [`docs/fontes.md`](docs/fontes.md) (R1 a R13: Cemig/Agência Minas, Procel, Idec, Inmetro/PBE, Komeco, MCTI, Enel SP/ANEEL e base SAMP da ANEEL).

## 10. Testes com usuários
Roteiro, ficha, formulário e registros em [`testes_usuarios/`](testes_usuarios/). Os testes automáticos de cálculo e do assistente ficam em `testes/`.

**Como foram aplicados:** cada participante usa o assistente com `python assistente/assistente.py --teste`, que registra de forma anônima o tempo para descobrir o gasto do chuveiro (S1), o número de erros de digitação e as opções usadas, sem salvar nenhum texto digitado. Depois responde a um formulário (compreensão e utilidade de 1 a 5, situações S1 a S4, dúvidas e sugestões). `python testes_usuarios/consolidar_testes.py` junta as duas fontes pelo código da sessão e gera `registro_testes.csv` e `resumo_testes.md`. Os participantes são identificados só por código e faixa etária, e separados em **grupo** e **externos**.

**Resultados e ajustes:** ver `testes_usuarios/resumo_testes.md`, `registro_testes.csv` e `CHANGELOG_MELHORIAS.md` (preenchidos apenas com sessões reais, sem dados pessoais). A amostra é pequena e não generaliza.

## 11. Limitações
Os resultados são estimativas e não garantem economia, geração ou custo. Não consideramos manutenção, financiamento, instalação extra, variação mensal entre verão e inverno nem mudanças futuras de tarifa. O caso de referência supera o consumo do domicílio médio da Enel SP, por isso o assistente recalcula com os dados do usuário. A Enel SP não atende toda a região metropolitana (por exemplo, o Alto Tietê é atendido pela EDP SP). A interface desta entrega é de terminal; para idosos, o ideal é a interface guiada ou por voz do Citizen Assist AI, que não foi implementada aqui (o módulo `modulo_energia.py` foi preparado para isso). O assistente é um protótipo educacional e não é canal oficial da Enel, da ANEEL ou do governo.

## 12. Uso de IA generativa
O grupo utilizou uma IA generativa apenas como apoio para estruturar o repositório, escrever partes de  código e rascunhar textos. A equipe é responsável pelos dados, cálculos, referências e recomendações apresentados e conferiu as fontes listadas em `docs/fontes.md`.
