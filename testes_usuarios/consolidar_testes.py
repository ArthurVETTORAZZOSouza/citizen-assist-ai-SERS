# -*- coding: utf-8 -*-
"""Junta os registros automáticos (sessoes/*.json) com as respostas do formulário (respostas_forms.csv)
e gera registro_testes.csv e resumo_testes.md.

Uso:
    1. Coloque na pasta sessoes/ os arquivos T-XXXX.json enviados pelos participantes.
    2. Baixe as respostas do formulário (Google Forms > Respostas > Planilha > Arquivo > Baixar > .csv)
       e salve como testes_usuarios/respostas_forms.csv.
    3. Rode:  python testes_usuarios/consolidar_testes.py

Rodar de novo é seguro: a coluna ajuste_gerado preenchida à mão é preservada. A ligação entre as duas fontes é o código da sessão (T-XXXX). Sessões sem formulário (ou formulários sem
sessão) entram mesmo assim, com um aviso, para você completar manualmente.
"""
import csv
import glob
import json
import os
import statistics
import unicodedata
from datetime import datetime

PASTA = os.path.dirname(os.path.abspath(__file__))
CAMPOS = ["codigo", "data", "grupo_ou_externo", "faixa_etaria", "situacoes_testadas", "compreensao_1a5",
          "utilidade_1a5", "tempo_s1_segundos", "erros_de_entrada", "comentarios", "ajuste_gerado"]


def normalizar(texto):
    sem = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    return " ".join(sem.lower().split())


def achar_coluna(cabecalhos, *trechos):
    """Devolve o cabeçalho que contém todos os trechos (comparação sem acento e sem maiúsculas)."""
    for c in cabecalhos:
        n = normalizar(c)
        if all(t in n for t in trechos):
            return c
    return None


def ler_sessoes(pasta):
    sessoes = {}
    for caminho in sorted(glob.glob(os.path.join(pasta, "*.json"))):
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        sessoes[dados["codigo"].strip().upper()] = dados
    return sessoes


def ler_forms(caminho):
    if not os.path.exists(caminho):
        return {}, {}
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        amostra = f.read(4096)
        f.seek(0)
        delimitador = ";" if amostra.count(";") > amostra.count(",") else ","
        leitor = csv.DictReader(f, delimiter=delimitador)
        cabecalhos = leitor.fieldnames or []
        col = {
            "codigo": achar_coluna(cabecalhos, "codigo da sessao"),
            "grupo": achar_coluna(cabecalhos, "grupo do projeto"),
            "faixa": achar_coluna(cabecalhos, "faixa etaria"),
            "s1": achar_coluna(cabecalhos, "s1."),
            "s2": achar_coluna(cabecalhos, "s2."),
            "s3": achar_coluna(cabecalhos, "s3."),
            "s4": achar_coluna(cabecalhos, "s4."),
            "compreensao": achar_coluna(cabecalhos, "entendi o que o assistente"),
            "utilidade": achar_coluna(cabecalhos, "me ajudariam"),
            "confuso": achar_coluna(cabecalhos, "confuso"),
            "sugestoes": achar_coluna(cabecalhos, "sugest"),
        }
        faltando = [k for k, v in col.items() if v is None]
        respostas = {}
        for linha in leitor:
            codigo = (linha.get(col["codigo"]) or "").strip().upper() if col["codigo"] else ""
            if codigo:
                respostas[codigo] = {k: (linha.get(v, "").strip() if v else "") for k, v in col.items()}
    return respostas, {"faltando": faltando}


def montar_linhas(sessoes, forms):
    codigos = sorted(set(sessoes) | set(forms))
    linhas, avisos = [], []
    for cod in codigos:
        s, r = sessoes.get(cod), forms.get(cod)
        if not s:
            avisos.append(f"{cod}: há respostas do formulário, mas não há arquivo de sessão (tempo e erros em branco; preencher à mão).")
        if not r:
            avisos.append(f"{cod}: há registro automático, mas não há resposta no formulário (notas e comentários em branco).")
        situacoes, partes = [], []
        if r:
            for chave, rotulo in (("s1", "S1"), ("s2", "S2"), ("s3", "S3"), ("s4", "S4")):
                resp = r.get(chave, "")
                if resp and "nao testei" not in normalizar(resp):
                    situacoes.append(rotulo)
                partes.append(f"{rotulo}: {resp or 'sem resposta'}.")
            if r.get("confuso"):
                partes.append(f"Confuso/dúvidas: {r['confuso']}.")
            if r.get("sugestoes"):
                partes.append(f"Sugestões: {r['sugestoes']}.")
        data = ""
        if s:
            data = datetime.fromisoformat(s["inicio"]).strftime("%d/%m/%Y")
        grupo = ""
        if r and r.get("grupo"):
            grupo = "grupo" if normalizar(r["grupo"]).startswith("sim") else "externo"
        linhas.append({
            "codigo": cod, "data": data, "grupo_ou_externo": grupo, "faixa_etaria": (r or {}).get("faixa", ""),
            "situacoes_testadas": ";".join(situacoes),
            "compreensao_1a5": (r or {}).get("compreensao", ""), "utilidade_1a5": (r or {}).get("utilidade", ""),
            "tempo_s1_segundos": "" if not s or s.get("tempo_s1_segundos") is None else s["tempo_s1_segundos"],
            "erros_de_entrada": "" if not s else s["erros_de_entrada"],
            "comentarios": " ".join(partes), "ajuste_gerado": "",
        })
    return linhas, avisos


def _numeros(linhas, campo):
    out = []
    for l in linhas:
        try:
            out.append(float(str(l[campo]).replace(",", ".")))
        except ValueError:
            pass
    return out


def resumo(linhas):
    n = len(linhas)
    g = sum(1 for l in linhas if l["grupo_ou_externo"] == "grupo")
    e = sum(1 for l in linhas if l["grupo_ou_externo"] == "externo")
    comp, util, t1, err = (_numeros(linhas, c) for c in ("compreensao_1a5", "utilidade_1a5", "tempo_s1_segundos", "erros_de_entrada"))
    media = lambda v: f"{statistics.mean(v):.1f}".replace(".", ",") if v else "sem dados"
    mediana = lambda v: f"{statistics.median(v):.0f}".replace(".", ",") if v else "sem dados"
    s1_sozinho = sum(1 for l in linhas if "s1: sozinho" in normalizar(l["comentarios"]))
    md = [
        "# Resumo dos testes com usuários (gerado por consolidar_testes.py)\n",
        f"* Participantes: **{n}** ({g} do grupo e {e} externos).",
        f"* Compreensão (1 a 5): média **{media(comp)}** ({len(comp)} respostas).",
        f"* Utilidade (1 a 5): média **{media(util)}** ({len(util)} respostas).",
        f"* Tempo para descobrir o gasto do chuveiro (S1): mediana **{mediana(t1)} s** ({len(t1)} sessões com registro automático).",
        f"* Erros de digitação por sessão: média **{media(err)}**; total {int(sum(err))}.",
        f"* Concluíram a S1 sozinhos: {s1_sozinho} de {n}.",
        "",
        "Atenção: amostra pequena e não aleatória. Os números descrevem estas sessões e não generalizam para a população.",
        "O tempo da S1 é medido automaticamente, da entrada na opção 1 até a exibição do custo mensal.",
        "",
        "## Frase para o vídeo e o README",
        f"\"Testamos com {n} pessoas ({g} do grupo e {e} externas). A compreensão média foi {media(comp)} e a utilidade, {media(util)}, "
        f"em escala de 1 a 5; o tempo mediano para descobrir o gasto do chuveiro foi de {mediana(t1)} segundos.\"",
        "",
        "## Comentários recebidos (use para preencher CHANGELOG_MELHORIAS.md)",

    ]
    for l in linhas:
        md.append(f"* **{l['codigo']}** ({l['grupo_ou_externo'] or '?'}, {l['faixa_etaria'] or '?'}): {l['comentarios']}")
    return "\n".join(md) + "\n"


def main(pasta=PASTA):
    sessoes = ler_sessoes(os.path.join(pasta, "sessoes"))
    forms, info = ler_forms(os.path.join(pasta, "respostas_forms.csv"))
    if info.get("faltando"):
        print("ATENÇÃO: não encontrei estas colunas no CSV do formulário:", ", ".join(info["faltando"]))
    linhas, avisos = montar_linhas(sessoes, forms)
    # preserva a coluna "ajuste_gerado" preenchida à mão em execuções anteriores
    anterior = os.path.join(pasta, "registro_testes.csv")
    if os.path.exists(anterior):
        with open(anterior, encoding="utf-8", newline="") as f:
            antigos = {l.get("codigo", "").strip().upper(): l.get("ajuste_gerado", "") for l in csv.DictReader(f)}
        for l in linhas:
            l["ajuste_gerado"] = antigos.get(l["codigo"], "")
    with open(os.path.join(pasta, "registro_testes.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(linhas)
    with open(os.path.join(pasta, "resumo_testes.md"), "w", encoding="utf-8") as f:
        f.write(resumo(linhas))
    print(f"{len(linhas)} sessões consolidadas em registro_testes.csv e resumo_testes.md")
    for a in avisos:
        print("AVISO:", a)
    return linhas, avisos


if __name__ == "__main__":
    main()
