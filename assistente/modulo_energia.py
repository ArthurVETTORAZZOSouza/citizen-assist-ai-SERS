# -*- coding: utf-8 -*-
"""Ponto de integração do módulo de Energia com o Citizen Assist AI.

Este arquivo expõe o módulo como funções puras (sem input() nem print()), para que outro assistente,
interface (terminal, web, voz) ou disciplina possa usar as mesmas respostas e os mesmos cálculos.

Exemplo de uso em outro assistente:

    import sys; sys.path.insert(0, "assistente")
    from modulo_energia import responder_energia, calcular_banho, comparar_banho

    r = responder_energia("aquecedor solar compensa?")
    print(r["texto"], r["referencias"], r["aviso"])

    c = comparar_banho(potencia_w=5500, minutos_atual=12, minutos_consciente=8, pessoas=4, tarifa=1.01)
    for alternativa in c["alternativas"]:
        print(alternativa["alternativa"], alternativa["economia_ano_rs"])

Todas as respostas trazem o aviso de estimativa e as referências, como exige o desafio.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assistente as _a  # noqa: E402

en = _a.en
P = _a.P
AVISO = _a.AVISO


def _validar(nome, valor, minimo, maximo):
    try:
        v = float(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{nome} deve ser um número entre {minimo:g} e {maximo:g}.")
    if v != v or v < minimo or v > maximo:
        raise ValueError(f"{nome} deve estar entre {minimo:g} e {maximo:g}.")
    return v


def responder_energia(pergunta):
    """Responde uma pergunta em texto livre sobre energia no banho.

    Retorna {"topico": id ou None, "texto": str, "referencias": [str], "aviso": str}.
    Perguntas fora do escopo retornam topico None e uma mensagem de orientação.
    """
    topico_id = _a.responder_texto(str(pergunta))
    if topico_id is None:
        return {"topico": None,
                "texto": ("Não encontrei uma resposta para isso. Posso ajudar com gasto do chuveiro, dicas de economia, "
                          "aquecedor solar, emissões, tarifa e dados da Enel SP."),
                "referencias": [], "aviso": AVISO}
    topico = next(t for t in _a.BASE["topicos"] if t["id"] == topico_id)
    return {"topico": topico_id, "texto": topico["resposta"],
            "referencias": [f"[{i}] {_a.BASE['referencias'][i]}" for i in topico["referencias"]],
            "aviso": AVISO}


def calcular_banho(potencia_w, minutos, pessoas, tarifa=None):
    """Energia (kWh/mês) e custo (R$) do chuveiro. Sem tarifa, usa a estimativa com tributos da Enel SP."""
    potencia_w = _validar("potencia_w", potencia_w, 1000, 8000)
    minutos = _validar("minutos", minutos, 1, 60)
    pessoas = _validar("pessoas", pessoas, 1, 12)
    tarifa = _a.TARIFA_PADRAO if tarifa is None else _validar("tarifa", tarifa, 0.2, 3.0)
    kwh = en.energia_kwh_mes(potencia_w, minutos, pessoas, P["dias_mes"])
    custo = en.custo_rs(kwh, tarifa)
    return {"kwh_mes": kwh, "custo_mes_rs": custo, "custo_ano_rs": 12 * custo, "tarifa_rs_kwh": tarifa,
            "referencias": [f"[{i}] {_a.BASE['referencias'][i]}" for i in ("R1", "R3")], "aviso": AVISO}


def comparar_banho(potencia_w, minutos_atual, minutos_consciente, pessoas, tarifa=None, orcamento=None):
    """Compara situação atual, A) uso consciente, B) aquecedor solar e A+B em três cenários solares.

    Com `orcamento` (R$), o custo do sistema solar passa a ser o orçamento informado nos três cenários.
    Retorna {"alternativas": [...cenário base...], "cenarios_solares": {nome: linha B}, "aviso": str, "referencias": [str]}.
    """
    potencia_w = _validar("potencia_w", potencia_w, 1000, 8000)
    minutos_atual = _validar("minutos_atual", minutos_atual, 1, 60)
    minutos_consciente = _validar("minutos_consciente", minutos_consciente, 1, minutos_atual)
    pessoas = _validar("pessoas", pessoas, 1, 12)
    tarifa = _a.TARIFA_PADRAO if tarifa is None else _validar("tarifa", tarifa, 0.2, 3.0)
    cenarios = en.cenarios_solares(P)
    if orcamento is not None:
        custo = _validar("orcamento", orcamento, 500, 30000)
        for c in cenarios.values():
            c["custo"] = custo
    base = cenarios["base"]
    alternativas = en.comparar_alternativas(potencia_w, minutos_atual, minutos_consciente, pessoas, tarifa,
                                            base["fracao"], base["custo"], P)
    solares = {nome: en.comparar_alternativas(potencia_w, minutos_atual, minutos_consciente, pessoas, tarifa,
                                              c["fracao"], c["custo"], P)[2] for nome, c in cenarios.items()}
    return {"alternativas": alternativas, "cenarios_solares": solares,
            "referencias": [f"[{i}] {_a.BASE['referencias'][i]}" for i in ("R1", "R3", "R4", "R12")],
            "aviso": AVISO}
