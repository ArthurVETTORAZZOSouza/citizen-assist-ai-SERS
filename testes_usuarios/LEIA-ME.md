# Testes com usuários

Esta pasta guarda o roteiro e os registros reais. Os arquivos `registro_testes.csv` 
começa **vazio de propósito**: deve ser preenchido apenas com testes que de fato aconteceram.
Para a demonstração automática das entradas inválidas, rode `python assistente/assistente.py --demo`.

Use `ficha_sessao.md` para anotar cada sessão e transformá-la em uma linha de `registro_testes.csv`.

Fluxo automatizado: (formulário e mensagens prontas) -> participantes rodam `python assistente/assistente.py --teste`
-> arquivos em `sessoes/` + CSV do formulário em `respostas_forms.csv` -> `python testes_usuarios/consolidar_testes.py`
gera `registro_testes.csv` e `resumo_testes.md`.
