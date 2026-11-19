# -*- coding: utf-8 -*-
"""Gera a comparação das alternativas para o domicílio de referência (4 pessoas, Enel SP).

Saídas em calculos/resultados/:
  comparacao_cenarios.csv, sensibilidade_tarifa.csv, sensibilidade_moradores.csv,
  sensibilidade_fracao_solar.csv, resumo_comparacao.md e (se o matplotlib estiver instalado) dois gráficos.
Uso: python calculos/comparacao_alternativas.py
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import energia as en

PASTA = os.path.join(en.RAIZ, "calculos", "resultados")
os.makedirs(PASTA, exist_ok=True)
p = en.carregar_premissas()
tarifa = en.tarifa_com_tributos_estimada(p)
cenarios = en.cenarios_solares(p)

CAMPOS = ["cenario", "alternativa", "kwh_mes", "custo_mes_rs", "custo_ano_rs", "economia_kwh_ano",
          "economia_ano_rs", "investimento_rs", "payback_anos", "custo_total_horizonte_rs", "co2_evitado_kg_ano"]


def fmt(x, d=2):
    if x is None:
        return "-"
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def salvar_csv(nome, linhas, campos):
    with open(os.path.join(PASTA, nome), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for l in linhas:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in l.items() if k in campos})


def comparar(tarifa_x, fracao, custo, pessoas=None, fator=None):
    return en.comparar_alternativas(
        p["potencia_chuveiro_w"], p["minutos_banho_atual"], p["minutos_banho_consciente"],
        p["pessoas"] if pessoas is None else pessoas, tarifa_x, fracao, custo, p, fator_emissao=fator)


# ---- 1) comparação principal: 3 cenários solares, tarifa estimada ----
todas = []
for nome, c in cenarios.items():
    for linha in comparar(tarifa, c["fracao"], c["custo"]):
        linha["cenario"] = nome
        todas.append(linha)
salvar_csv("comparacao_cenarios.csv", todas, CAMPOS)

# ---- 2) sensibilidade à tarifa (cenário base) ----
sens_tarifa = []
for t in (0.80, round(tarifa, 4), 1.20):
    c = cenarios["base"]
    for l in comparar(t, c["fracao"], c["custo"]):
        l["cenario"] = f"tarifa R$ {t:.2f}/kWh"
        sens_tarifa.append(l)
salvar_csv("sensibilidade_tarifa.csv", sens_tarifa, CAMPOS)

# ---- 3) sensibilidade ao número de moradores (cenário base) ----
sens_pessoas = []
for n in (2, 3, 4, 5):
    c = cenarios["base"]
    for l in comparar(tarifa, c["fracao"], c["custo"], pessoas=n):
        l["cenario"] = f"{n} moradores"
        sens_pessoas.append(l)
salvar_csv("sensibilidade_moradores.csv", sens_pessoas, CAMPOS)

# ---- 4) sensibilidade à fração solar (custo base) ----
sens_fracao = []
for f_ in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
    for l in comparar(tarifa, f_, cenarios["base"]["custo"]):
        l["cenario"] = f"fração solar {int(f_ * 100)}%"
        sens_fracao.append(l)
salvar_csv("sensibilidade_fracao_solar.csv", sens_fracao, CAMPOS)

# ---- 5) verificação cruzada com a simulação da Cemig (R1) ----
kwh_cemig = en.energia_kwh_mes(5500, 12, 4) - en.energia_kwh_mes(5500, 8, 4)
tarifa_implicita_cemig = 50.54 / kwh_cemig

# ---- 6) resumo em markdown ----
base = [l for l in todas if l["cenario"] == "base"]
atual, a, b, ab = base
prod = en.producao_solar_nominal_kwh_mes(p)
Bc = [x for x in todas if x["cenario"] == "conservador" and x["alternativa"].startswith("B)")][0]
Bo = [x for x in todas if x["cenario"] == "otimista" and x["alternativa"].startswith("B)")][0]
kwh_atual = atual["kwh_mes"]
md = []
md.append("# Resumo da comparação de alternativas (gerado por calculos/comparacao_alternativas.py)\n")
md.append(f"Domicílio de referência: {int(p['pessoas'])} moradores, chuveiro de {int(p['potencia_chuveiro_w'])} W, "
          f"banho de {int(p['minutos_banho_atual'])} min por pessoa por dia, {int(p['dias_mes'])} dias por mês. "
          f"Tarifa com tributos **estimada**: R$ {fmt(tarifa, 4)}/kWh. Período de referência: 12 meses e {int(p['horizonte_anos'])} anos.\n")
md.append("## Cenário base (todas as alternativas para a mesma necessidade)\n")
md.append("| Alternativa | kWh/mês | Custo/mês (R$) | Economia/ano (R$) | Investimento (R$) | Retorno (anos) | Custo total em 10 anos (R$) | CO2 evitado (kg/ano) |")
md.append("|---|---|---|---|---|---|---|---|")
for l in base:
    md.append(f"| {l['alternativa']} | {fmt(l['kwh_mes'], 1)} | {fmt(l['custo_mes_rs'])} | {fmt(l['economia_ano_rs'])} | "
              f"{fmt(l['investimento_rs'], 0)} | {fmt(l['payback_anos'], 1)} | {fmt(l['custo_total_horizonte_rs'], 0)} | {fmt(l['co2_evitado_kg_ano'], 1)} |")
md.append("\n## Aquecedor solar (alternativa B) nos três cenários\n")
md.append("| Cenário | Fração solar | Custo do sistema (R$) | Economia/ano (R$) | Retorno (anos) | Custo total em 10 anos (R$) | CO2 evitado (kg/ano) |")
md.append("|---|---|---|---|---|---|---|")
for nome, c in cenarios.items():
    l = [x for x in todas if x["cenario"] == nome and x["alternativa"].startswith("B)")][0]
    md.append(f"| {nome} | {int(c['fracao'] * 100)}% | {fmt(c['custo'], 0)} | {fmt(l['economia_ano_rs'])} | "
              f"{fmt(l['payback_anos'], 1)} | {fmt(l['custo_total_horizonte_rs'], 0)} | {fmt(l['co2_evitado_kg_ano'], 1)} |")
md.append("\n## Verificações de consistência\n")
md.append(f"* Coletor de referência (R12): {fmt(p['solar_area_m2'], 2)} m2 x {fmt(p['solar_pmee_kwh_m2_mes'], 2)} kWh/m2.mês = "
          f"{fmt(p['solar_area_m2'] * p['solar_pmee_kwh_m2_mes'], 1)} kWh/mês nominais; com fator de perdas de {fmt(p['solar_fator_sistema'], 1)}, "
          f"**{fmt(prod, 1)} kWh/mês**, contra uma demanda de {fmt(kwh_atual, 1)} kWh/mês ({fmt(100 * prod / kwh_atual, 0)}% da demanda). "
          f"Os cenários de fração solar (50%, 60% e 70%) ficam abaixo dessa produção, e o otimista coincide com a alegação máxima do fabricante (até 70%).")
md.append(f"* Simulação da Cemig (R1): reduzir o banho de 12 para 8 min poupa {fmt(kwh_cemig, 1)} kWh/mês; a economia divulgada de R$ 50,54 "
          f"implica uma tarifa de R$ {fmt(tarifa_implicita_cemig, 2)}/kWh (com tributos, distribuidora de Minas Gerais). "
          f"A tarifa estimada para a Enel SP (R$ {fmt(tarifa, 2)}/kWh) é da mesma ordem de grandeza.")
md.append(f"* Retorno: base {fmt(b['payback_anos'], 1)} anos e otimista {fmt(Bo['payback_anos'], 1)} anos ficam dentro da faixa de 2 a 7 anos do Idec (R3); "
          f"o conservador ({fmt(Bc['payback_anos'], 1)} anos) fica fora dela e é apresentado como limite inferior.")
md.append("\n## Limites\n")
md.append("* Não modela a variação entre verão e inverno mês a mês, nem manutenção, financiamento ou custo de instalação extra.")
md.append("* O cenário-base é um caso de referência (simulação da Cemig); ele supera o consumo do domicílio médio da Enel SP. "
          "O assistente recalcula com os dados informados pelo usuário.")
md.append("* Estimativas de economia, geração e custos não são resultados garantidos.\n")
with open(os.path.join(PASTA, "resumo_comparacao.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# ---- 7) gráficos (opcionais) ----
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    nomes = ["Atual", "A) Uso\nconsciente", "B) Aquecedor\nsolar", "A+B"]
    cores = ["#9e9e9e", "#2171b5", "#d94801", "#238b45"]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    custos = [l["custo_ano_rs"] for l in base]
    barras = ax.bar(nomes, custos, color=cores)
    for barra, v in zip(barras, custos):
        ax.text(barra.get_x() + barra.get_width() / 2, v + 20, f"R$ {v:,.0f}".replace(",", "."), ha="center", fontsize=9)
    ax.set_ylabel("Custo anual do banho quente (R$)")
    ax.set_title("Custo anual do banho quente, domicílio de referência (cenário base)")
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA, "grafico_custo_anual.png"), dpi=150)
    plt.close()

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    anos = list(range(0, int(p["horizonte_anos"]) + 1))
    for l, nome, cor in zip(base, nomes, cores):
        ax.plot(anos, [l["investimento_rs"] + a_ * l["custo_ano_rs"] for a_ in anos], label=nome.replace("\n", " "), color=cor, lw=2)
    ax.set_xlabel("Anos")
    ax.set_ylabel("Custo acumulado (R$)")
    ax.set_title("Custo acumulado em 10 anos (investimento + conta de luz do banho)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA, "grafico_custo_acumulado.png"), dpi=150)
    plt.close()
    print("Gráficos gerados.")
except ImportError:
    print("matplotlib não instalado: gráficos não gerados (os CSVs e o resumo foram criados).")

print("\n".join(md))
