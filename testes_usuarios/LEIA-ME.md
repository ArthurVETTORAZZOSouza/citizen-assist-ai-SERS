# Testes com usuários

Esta pasta guarda o roteiro e os registros reais. Os arquivos `registro_testes.csv` e `ajustes_realizados.md`
começam **vazios de propósito**: devem ser preenchidos apenas com testes que de fato aconteceram.
Para a demonstração automática das entradas inválidas, rode `python assistente/assistente.py --demo`.

Use `ficha_sessao.md` para anotar cada sessão e transformá-la em uma linha de `registro_testes.csv`.

Fluxo automatizado: `mensagem_whatsapp.md` (formulário e mensagens prontas) -> participantes rodam `python assistente/assistente.py --teste`
-> arquivos em `sessoes/` + CSV do formulário em `respostas_forms.csv` -> `python testes_usuarios/consolidar_testes.py`
gera `registro_testes.csv` e `resumo_testes.md`.
