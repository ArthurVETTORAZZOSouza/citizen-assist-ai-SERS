# Testes com usuários

Esta pasta guarda o roteiro e os registros reais dos testes de usabilidade aplicados ao protótipo. Os arquivos `registro_testes.csv` e `resumo_testes.md` consolidam apenas sessões que de fato aconteceram, sem dados pessoais, e os ajustes gerados no código e na base de conhecimento estão documentados em `../CHANGELOG_MELHORIAS.md`. Para a demonstração automática com entradas inválidas, rode `python assistente/assistente.py --demo`.

Use `ficha_sessao.md` caso queira registrar uma sessão manualmente em `registro_testes.csv`.

Fluxo automatizado utilizado: participantes rodam `python assistente/assistente.py --teste` (gerando os registros anônimos em `sessoes/`) e respondem ao formulário (exportado em `respostas_forms.csv`). Em seguida, `python testes_usuarios/consolidar_testes.py` cruza as duas fontes pelo código da sessão e gera `registro_testes.csv` e `resumo_testes.md`.
