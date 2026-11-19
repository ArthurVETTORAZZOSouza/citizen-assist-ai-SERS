# -*- coding: utf-8 -*-
"""Funções de cálculo do módulo de energia do Citizen Assist AI.

Conceitos usados (todos explicados no README):
  * Potência (P, em kW) é a energia consumida por unidade de tempo.
  * Energia (E, em kWh) = P (kW) x tempo (h).
  * Custo (R$) = E (kWh) x tarifa (R$/kWh).
  * Chuveiro elétrico: resistência com rendimento próximo de 100% (toda a energia elétrica vira calor).
  * Aquecedor solar: o coletor transfere calor do sol para a água; a rede elétrica só complementa.
  * Emissões evitadas (kg CO2) = energia elétrica evitada (kWh) x fator de emissão da rede (kg CO2/kWh).

Todos os parâmetros vêm de dados/premissas.csv (única fonte de verdade).
"""
import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ_PREMISSAS = os.path.join(RAIZ, "dados", "premissas.csv")


def carregar_premissas(caminho=ARQ_PREMISSAS):
    """Lê dados/premissas.csv e devolve {id: valor numérico}."""
    premissas = {}
    with open(caminho, encoding="utf-8", newline="") as arq:
        for linha in csv.DictReader(arq):
            premissas[linha["id"]] = float(linha["valor"])
    return premissas


def energia_kwh_mes(potencia_w, minutos_por_banho, pessoas, dias=30):
    """Energia do chuveiro em kWh/mês, com um banho por pessoa por dia."""
    return (potencia_w / 1000.0) * (minutos_por_banho / 60.0) * pessoas * dias


def custo_rs(kwh, tarifa_rs_kwh):
    return kwh * tarifa_rs_kwh


def tarifa_com_tributos_estimada(p):
    """Tarifa com tributos (R$/kWh) = (TUSD + TE com tributos) x (1 + reajuste B1 de 2026). ESTIMADA."""
    return (p["tarifa_tusd_com_tributos"] + p["tarifa_te_com_tributos"]) * (1.0 + p["reajuste_b1_2026"])


def co2_kg(kwh, fator_kg_kwh):
    return kwh * fator_kg_kwh


def payback_anos(investimento_rs, economia_ano_rs):
    """Tempo de retorno simples (anos). Devolve None quando não há investimento ou economia."""
    if investimento_rs <= 0 or economia_ano_rs <= 0:
        return None
    return investimento_rs / economia_ano_rs


def producao_solar_nominal_kwh_mes(p):
    """Produção nominal do sistema de referência: área x PMEe x fator de perdas."""
    return p["solar_area_m2"] * p["solar_pmee_kwh_m2_mes"] * p["solar_fator_sistema"]


def cenarios_solares(p):
    """Cenários de custo e fração solar (todos ESTIMADOS)."""
    return {
        "conservador": {"fracao": p["solar_fracao_conservador"], "custo": p["solar_custo_conservador"]},
        "base": {"fracao": p["solar_fracao_base"], "custo": p["solar_custo_base"]},
        "otimista": {"fracao": p["solar_fracao_otimista"], "custo": p["solar_custo_otimista"]},
    }


def comparar_alternativas(potencia_w, minutos_atual, minutos_consciente, pessoas, tarifa,
                          fracao_solar, custo_solar, p, dias=None, fator_emissao=None, horizonte=None):
    """Compara, para a MESMA necessidade (banho quente do domicílio) e o MESMO período (12 meses e horizonte
    de anos), a situação atual com duas alternativas e a combinação delas.

    Retorna uma lista de dicionários, um por alternativa.
    """
    dias = p["dias_mes"] if dias is None else dias
    fator = p["fator_emissao_kg_kwh"] if fator_emissao is None else fator_emissao
    anos = p["horizonte_anos"] if horizonte is None else horizonte

    kwh_atual = energia_kwh_mes(potencia_w, minutos_atual, pessoas, dias)
    kwh_a = energia_kwh_mes(potencia_w, minutos_consciente, pessoas, dias)
    kwh_b = kwh_atual * (1.0 - fracao_solar)
    kwh_ab = kwh_a * (1.0 - fracao_solar)

    definicoes = [
        ("Situação atual (chuveiro elétrico)", kwh_atual, 0.0),
        ("A) Uso consciente (banho mais curto)", kwh_a, 0.0),
        ("B) Aquecedor solar com apoio elétrico", kwh_b, custo_solar),
        ("A+B) Uso consciente e aquecedor solar", kwh_ab, custo_solar),
    ]
    linhas = []
    for nome, kwh, investimento in definicoes:
        custo_mes = custo_rs(kwh, tarifa)
        custo_ano = 12.0 * custo_mes
        economia_kwh_ano = 12.0 * (kwh_atual - kwh)
        economia_ano = custo_rs(economia_kwh_ano, tarifa)
        linhas.append({
            "alternativa": nome,
            "kwh_mes": kwh,
            "custo_mes_rs": custo_mes,
            "custo_ano_rs": custo_ano,
            "economia_kwh_ano": economia_kwh_ano,
            "economia_ano_rs": economia_ano,
            "investimento_rs": investimento,
            "payback_anos": payback_anos(investimento, economia_ano),
            "custo_total_horizonte_rs": investimento + anos * custo_ano,
            "co2_evitado_kg_ano": co2_kg(economia_kwh_ano, fator),
        })
    return linhas
