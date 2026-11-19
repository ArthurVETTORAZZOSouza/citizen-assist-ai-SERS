# Roteiro dos testes com usuários

Objetivo: verificar se as orientações do assistente são **compreensíveis** e **úteis**, e registrar os ajustes feitos.

## Regras
* Não coletar nome, telefone, endereço, número de conta ou qualquer dado pessoal. Identificar cada participante só por um código (T01, T02, ...), com a **faixa etária** e se é **do grupo** ou **externo**.
* Explicar antes: "É um protótipo educacional, as respostas são estimativas e você pode parar quando quiser."
* Cada sessão leva cerca de 10 minutos. O participante usa o assistente sozinho; o aplicador só observa e anota.
* Registrar tudo em `registro_testes.csv`, **exatamente como aconteceu**, inclusive os problemas. Não preencher testes que não foram feitos.

## Situações testadas
| Código | Situação pedida ao participante | O que observar |
|---|---|---|
| S1 | "Descubra quanto o seu chuveiro gasta por mês." | Entendeu as 4 perguntas? Soube a potência? Errou alguma entrada? |
| S2 | "Veja se vale a pena trocar por aquecedor solar." | Entendeu a tabela de comparação? Entendeu o aviso de estimativa? |
| S3 | "Pergunte, com as suas palavras, como economizar no banho." | O assistente entendeu? A resposta foi clara? |
| S4 | "Digite algo que não faça sentido (letras onde pede número)." | A mensagem de erro ajudou? |

## Perguntas após as situações
1. **Compreensão** (1 a 5): "Entendi o que o assistente me disse."
2. **Utilidade** (1 a 5): "As orientações me ajudariam a decidir como economizar."
3. **Tempo** (segundos) para encontrar a informação pedida em S1.
4. Aberta: "O que foi confuso?" e "O que você mudaria?"

## Escala
1 = discordo totalmente, 3 = neutro, 5 = concordo totalmente.

## Depois de cada sessão
Anotar em `ajustes_realizados.md` qual comentário gerou qual mudança no assistente (ou por que não mudou).
