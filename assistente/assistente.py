# -*- coding: utf-8 -*-
"""Citizen Assist AI | módulo de Energia (Soluções em Energias Renováveis e Sustentáveis).

Assistente de terminal sobre uso consciente de energia no banho. Não coleta dados pessoais e não é canal oficial.

Uso:
    python assistente/assistente.py          # modo interativo
    python assistente/assistente.py --demo   # demonstração roteirizada (inclui entradas inválidas)
    python assistente/assistente.py --teste  # uso normal + registro anônimo para os testes com usuários
"""
import builtins
import csv
import datetime
import json
import os
import re
import secrets
import sys
import time
import unicodedata

PASTA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(PASTA)
sys.path.insert(0, os.path.join(RAIZ, "calculos"))
import energia as en  # noqa: E402

P = en.carregar_premissas()
TARIFA_PADRAO = round(en.tarifa_com_tributos_estimada(P), 2)
with open(os.path.join(PASTA, "base_conhecimento.json"), encoding="utf-8") as _f:
    BASE = json.load(_f)

AVISO = ("AVISO: estimativa educacional, não é garantia de economia, geração ou custo. "
         "O resultado real depende da sua conta, do clima e do orçamento da instalação.")


class Sessao:
    """Registro ANÔNIMO de uma sessão de teste (modo --teste).

    Guarda apenas tempos, contagens e opções usadas. Nenhum texto digitado pelo usuário é salvo.
    """

    def __init__(self):
        alfabeto = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        self.codigo = "T-" + "".join(secrets.choice(alfabeto) for _ in range(4))
        self.inicio = datetime.datetime.now()
        self.erros = 0
        self.opcoes = []
        self.topicos = []
        self.perguntas_sem_resposta = 0
        self.t_s1_inicio = None
        self.t_s1 = None

    def salvar(self, pasta=None):
        pasta = pasta or os.path.join(RAIZ, "testes_usuarios", "sessoes")
        os.makedirs(pasta, exist_ok=True)
        fim = datetime.datetime.now()
        dados = {
            "codigo": self.codigo,
            "inicio": self.inicio.isoformat(timespec="seconds"),
            "fim": fim.isoformat(timespec="seconds"),
            "duracao_total_s": round((fim - self.inicio).total_seconds(), 1),
            "opcoes_usadas": self.opcoes,
            "erros_de_entrada": self.erros,
            "tempo_s1_segundos": self.t_s1,
            "perguntas_livres_topicos": self.topicos,
            "perguntas_livres_sem_resposta": self.perguntas_sem_resposta,
        }
        caminho = os.path.join(pasta, f"{self.codigo}.json")
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return caminho


SESSAO = None  # só é criada com a opção --teste


def _erro():
    if SESSAO:
        SESSAO.erros += 1


def _inicio_s1():
    if SESSAO and SESSAO.t_s1_inicio is None:
        SESSAO.t_s1_inicio = time.monotonic()


def _fim_s1():
    if SESSAO and SESSAO.t_s1 is None and SESSAO.t_s1_inicio is not None:
        SESSAO.t_s1 = round(time.monotonic() - SESSAO.t_s1_inicio, 1)


class VoltarAoMenu(Exception):
    """Levantada quando o usuário digita 'voltar' ou 'menu' em qualquer pergunta."""


def fmt(x, casas=2):
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sem_acento.lower().split())


def ler_numero(pergunta, minimo, maximo, padrao=None, tentativas=3):
    """Lê um número com validação. ENTER usa o padrão; 'voltar' retorna ao menu."""
    dica = f" [ENTER = {fmt(padrao, 2).rstrip('0').rstrip(',') if padrao is not None else 'sem padrão'}]"
    for tentativa in range(tentativas):
        bruto = input(f"{pergunta}{dica}: ").strip()
        if normalizar(bruto) in ("voltar", "menu"):
            raise VoltarAoMenu()
        if bruto == "" and padrao is not None:
            return float(padrao)
        try:
            valor = float(bruto.replace(",", "."))
        except ValueError:
            print(f"  Não entendi. Digite apenas um número, entre {fmt(minimo, 0)} e {fmt(maximo, 0)}.")
            _erro()
            continue
        if valor != valor or valor < minimo or valor > maximo:
            print(f"  Esse valor está fora do esperado. Digite um número entre {fmt(minimo, 0)} e {fmt(maximo, 0)}.")
            _erro()
            continue
        return valor
    if padrao is not None:
        print(f"  Vou usar o valor padrão ({fmt(padrao, 2)}) para continuar.")
        return float(padrao)
    raise VoltarAoMenu()


def ler_sim_nao(pergunta, padrao=True):
    resp = normalizar(input(f"{pergunta} [{'S/n' if padrao else 's/N'}]: "))
    if resp in ("voltar", "menu"):
        raise VoltarAoMenu()
    if resp == "":
        return padrao
    return resp.startswith("s")


def referencias_texto(ids):
    return "\n".join(f"  [{i}] {BASE['referencias'][i]}" for i in ids if i in BASE["referencias"])


def coletar_perfil(perfil):
    """Pergunta os dados do domicílio (sem nenhum dado pessoal)."""
    print("\nVou fazer 4 perguntas curtas. Digite ENTER para usar o valor sugerido.")
    perfil["potencia_w"] = ler_numero("1) Potência do chuveiro em watts (está na etiqueta do chuveiro)", 1000, 8000, P["potencia_chuveiro_w"])
    perfil["minutos"] = ler_numero("2) Quantos minutos dura um banho, por pessoa", 1, 60, P["minutos_banho_atual"])
    perfil["pessoas"] = ler_numero("3) Quantas pessoas tomam banho por dia", 1, 12, P["pessoas"])
    perfil["tarifa"] = ler_numero("4) Preço do kWh em reais, com tributos (está na sua conta de luz)", 0.2, 3.0, TARIFA_PADRAO)


def opcao_calcular(perfil):
    print("\n--- Quanto o chuveiro gasta por mês ---")
    _inicio_s1()
    coletar_perfil(perfil)
    kwh = en.energia_kwh_mes(perfil["potencia_w"], perfil["minutos"], perfil["pessoas"], P["dias_mes"])
    custo = en.custo_rs(kwh, perfil["tarifa"])
    print(f"\nCom {fmt(perfil['potencia_w'], 0)} W, {fmt(perfil['minutos'], 0)} min por banho e {fmt(perfil['pessoas'], 0)} pessoa(s):")
    print(f"  Energia do chuveiro: {fmt(kwh, 1)} kWh por mês")
    print(f"  Custo estimado:      R$ {fmt(custo)} por mês (R$ {fmt(12 * custo)} por ano)")
    print("  Como calculei: potência (kW) x tempo (h) x pessoas x 30 dias, e depois x preço do kWh.")
    _fim_s1()
    print(AVISO)
    print("Fontes:\n" + referencias_texto(["R1", "R2"]))


def opcao_comparar(perfil):
    print("\n--- Comparar: uso consciente x aquecedor solar ---")
    if not perfil or not ler_sim_nao("Usar os mesmos dados informados antes?", True):
        coletar_perfil(perfil)
    minutos_consc = ler_numero("Quantos minutos teria o banho no uso consciente", 1, perfil["minutos"], min(P["minutos_banho_consciente"], perfil["minutos"]))
    cen = en.cenarios_solares(P)
    custo_estimado = cen["base"]["custo"]
    print("\nSe você já tem o orçamento de um aquecedor solar, digite o valor. O Idec indica que o preço depende do número de moradores.")
    orcamento = ler_numero("Valor do orçamento em reais", 500, 30000, custo_estimado)
    usou_orcamento = abs(orcamento - custo_estimado) > 1e-9
    if usou_orcamento:
        for c in cen.values():
            c["custo"] = orcamento
        print("  Vou usar o seu orçamento nos três cenários.")
    elif perfil["pessoas"] < 3:
        print(f"  Atenção: a estimativa de R$ {fmt(custo_estimado, 0)} foi pensada para {fmt(P['pessoas'], 0)} moradores; "
              "em casas menores o sistema pode custar menos. Prefira um orçamento real.")
    base = cen["base"]
    linhas = en.comparar_alternativas(perfil["potencia_w"], perfil["minutos"], minutos_consc, perfil["pessoas"],
                                      perfil["tarifa"], base["fracao"], base["custo"], P)
    print("\nMesma necessidade (banho quente da casa), período de 12 meses (cenário base):")
    print(f"  {'Alternativa':<42}{'Custo/mês':>12}{'Economia/ano':>15}")
    for l in linhas:
        print(f"  {l['alternativa']:<42}{'R$ ' + fmt(l['custo_mes_rs']):>12}{'R$ ' + fmt(l['economia_ano_rs']):>15}")
    b = linhas[2]
    print("\nAquecedor solar (alternativa renovável), três cenários de custo e de sol:")
    for nome, c in cen.items():
        l = en.comparar_alternativas(perfil["potencia_w"], perfil["minutos"], minutos_consc, perfil["pessoas"],
                                     perfil["tarifa"], c["fracao"], c["custo"], P)[2]
        retorno = f"{fmt(l['payback_anos'], 1)} anos" if l["payback_anos"] else "sem retorno"
        print(f"  {nome:<12} sol {int(c['fracao'] * 100):>3}% | sistema R$ {fmt(c['custo'], 0):>6} | economia R$ {fmt(l['economia_ano_rs']):>9}/ano | retorno {retorno}")
    print(f"\nImpacto ambiental (base): {fmt(b['co2_evitado_kg_ano'], 1)} kg de CO2 evitados por ano com o aquecedor solar.")
    print("Esse ganho de CO2 é pequeno porque a rede elétrica brasileira já é limpa; o principal benefício é financeiro.")
    print("Recomendação: comece pelo banho mais curto (custo zero) e peça orçamentos de aquecedor solar para decidir.")
    print(AVISO)
    print("Fontes:\n" + referencias_texto(["R1", "R3", "R4", "R5"]))


def mostrar_topico(topico_id):
    for t in BASE["topicos"]:
        if t["id"] == topico_id:
            print("\n" + t["resposta"])
            if t["referencias"]:
                print("Fontes:\n" + referencias_texto(t["referencias"]))
            return


def opcao_dicas():
    print("\n--- Dicas para economizar no banho ---")
    mostrar_topico("uso_consciente")
    mostrar_topico("baixa_renda")


def opcao_solar():
    print("\n--- Aquecedor solar: custo, retorno e limites ---")
    mostrar_topico("solar_custo")
    mostrar_topico("solar_como")
    print(AVISO)


def opcao_dados_enel():
    print("\n--- Dados reais da Enel SP (base SAMP da ANEEL, 2025) ---")
    caminho = os.path.join(RAIZ, "dados", "samp_enel_sp_2025.csv")
    with open(caminho, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    kwh = sum(float(l["kwh_tusd"]) for l in linhas)
    cons = sum(float(l["consumidores"]) for l in linhas)
    rec = sum(float(l["receita_energia"]) for l in linhas)
    h1 = [l for l in linhas if l["mes"] <= "2025-06"]
    h2 = [l for l in linhas if l["mes"] > "2025-06"]
    tar = lambda ls: sum(float(l["receita_energia"]) for l in ls) / sum(float(l["kwh_tusd"]) for l in ls)
    baixa = sum(float(l["pct_baixa_renda"]) for l in linhas) / len(linhas)
    print(f"  Consumo médio residencial: {fmt(kwh / cons, 1)} kWh por mês por consumidor (todos os usos da casa)")
    print(f"  Consumidores de baixa renda: cerca de {fmt(baixa, 1)}% dos residenciais")
    print(f"  Tarifa média sem tributos: R$ {fmt(tar(h1), 2)}/kWh (jan a jun) e R$ {fmt(tar(h2), 2)}/kWh (jul a dez)")
    print("  Para a conta real, some os tributos: por isso peço o valor do kWh da sua conta.")
    print("  Obs.: o chuveiro costuma ser uma das maiores parcelas da conta (pesquisas do Procel indicam 24% a 35%, dados antigos).")
    print("Fonte:\n" + referencias_texto(["R9", "R10"]))


def opcao_fontes():
    print("\n--- Fontes e limitações ---")
    mostrar_topico("limitacoes")
    print("\nTodas as fontes:\n" + referencias_texto(list(BASE["referencias"])))


def responder_texto(pergunta):
    """Entende uma pergunta livre por palavras-chave, ignorando termos negados."""
    texto = normalizar(pergunta[:300])
    if not texto:
        return None

    # Remove trechos logo após negações para evitar falsos positivos (ex: "não posso instalar solar")
    texto_filtrado = re.sub(r"\b(nao|sem|dispenso|nunca)\b[^,.;!?]*", "", texto).strip()
    if not texto_filtrado:
        texto_filtrado = texto

    melhor, pontos = None, 0
    for t in BASE["topicos"]:
        # expressões mais longas (ex.: "tarifa social") pesam mais que palavras soltas (ex.: "tarifa")
        p = sum(len(k) for k in t["palavras_chave"] if k in texto_filtrado)
        if p > pontos:
            melhor, pontos = t, p
    return melhor["id"] if melhor else None

def responder_texto(pergunta):
    """Entende uma pergunta livre por palavras-chave, ignorando termos negados."""
    texto = normalizar(pergunta[:300])
    if not texto:
        return None

    # Remove trechos logo após negações para evitar falsos positivos (ex: "não posso instalar solar")
    texto_filtrado = re.sub(r"\b(nao|sem|dispenso|nunca)\b[^,.;!?]*", "", texto).strip()
    if not texto_filtrado:
        texto_filtrado = texto

    melhor, pontos = None, 0
    for t in BASE["topicos"]:
        # expressões mais longas (ex.: "tarifa social") pesam mais que palavras soltas (ex.: "tarifa")
        p = sum(len(k) for k in t["palavras_chave"] if k in texto_filtrado)
        if p > pontos:
            melhor, pontos = t, p
    return melhor["id"] if melhor else None


def opcao_pergunta(perfil):
    print("\n--- Pergunte com as suas palavras ---")
    pergunta = input("Digite sua pergunta (ou 'voltar'): ")
    if normalizar(pergunta) in ("voltar", "menu"):
        raise VoltarAoMenu()
    topico = responder_texto(pergunta)
    if SESSAO:
        if topico:
            SESSAO.topicos.append(topico)
        else:
            SESSAO.perguntas_sem_resposta += 1
    if topico is None:
        print("\nNão encontrei uma resposta para isso. Posso ajudar com gasto do chuveiro, dicas de economia,")
        print("aquecedor solar, emissões, tarifa e dados da Enel SP. Tente reformular ou use o menu.")
        return
    mostrar_topico(topico)


    if topico == "chave_verao_inverno" and perfil:
        kwh_atual = en.energia_kwh_mes(perfil["potencia_w"], perfil["minutos"], perfil["pessoas"], P["dias_mes"])
        custo_atual = en.custo_rs(kwh_atual, perfil["tarifa"])
        economia_verao = custo_atual * 0.30
        print(f"\n  [Seu perfil]: Com {fmt(perfil['potencia_w'], 0)} W, mudar para a posição Verão")
        print(f"  pode economizar cerca de R$ {fmt(economia_verao)} por mês (30% de redução).")

    elif topico == "solar_custo" and perfil:
        cen = en.cenarios_solares(P)["base"]
        linhas = en.comparar_alternativas(
            perfil["potencia_w"], perfil["minutos"], perfil["minutos"],
            perfil["pessoas"], perfil["tarifa"], cen["fracao"], cen["custo"], P
        )
        solar_base = linhas[2]
        retorno = f"{fmt(solar_base['payback_anos'], 1)} anos" if solar_base["payback_anos"] else "mais de 15 anos"
        print(
            f"\n  [Seu perfil]: Com {fmt(perfil['pessoas'], 0)} pessoa(s) e banho de {fmt(perfil['minutos'], 0)} min,")
        print(
            f"  um sistema base (R$ {fmt(cen['custo'], 0)}) economizaria R$ {fmt(solar_base['economia_ano_rs'])}/ano (retorno em {retorno}).")

    acao = next((t.get("acao") for t in BASE["topicos"] if t["id"] == topico), None)

    if acao == "calcular" and ler_sim_nao("Quer calcular com os seus dados agora?", True):
        opcao_calcular(perfil)
    elif acao == "comparar" and ler_sim_nao("Quer comparar as alternativas com os seus dados agora?", True):
        opcao_comparar(perfil)
    elif acao == "dados":
        opcao_dados_enel()



MENU = """
================ Citizen Assist AI | Energia ================
 1  Quanto o meu chuveiro gasta por mês?
 2  Comparar: uso consciente x aquecedor solar
 3  Dicas para economizar no banho
 4  Aquecedor solar: custo, retorno e limites
 5  Dados reais da Enel SP (2025)
 6  Fontes e limitações
 7  Perguntar com as minhas palavras
 0  Sair
Digite 'voltar' a qualquer momento para retornar a este menu.
==============================================================="""


def iniciar():
    print("\nOlá! Sou um protótipo educacional sobre uso consciente de energia.")
    print("Não sou canal oficial da Enel, da ANEEL ou do governo e não peço dados pessoais.")
    perfil = {}
    acoes = {"1": lambda: opcao_calcular(perfil), "2": lambda: opcao_comparar(perfil), "3": opcao_dicas,
             "4": opcao_solar, "5": opcao_dados_enel, "6": opcao_fontes, "7": lambda: opcao_pergunta(perfil)}
    while True:
        print(MENU)
        try:
            escolha = input("Escolha uma opção (0 a 7): ").strip()
        except EOFError:
            break
        if escolha == "0":
            print("\nObrigado por usar o assistente. Lembre-se: confirme os valores com a sua conta de luz.")
            break
        if escolha not in acoes:
            print("\nOpção inválida. Digite um número de 0 a 7.")
            _erro()
            continue
        if SESSAO:
            SESSAO.opcoes.append(escolha)
        try:
            acoes[escolha]()
        except VoltarAoMenu:
            print("\nVoltando ao menu.")
        except (EOFError, KeyboardInterrupt):
            break


def demo():
    """Roda uma conversa roteirizada, incluindo entradas inválidas (usada nos testes e no vídeo)."""
    roteiro = iter([
        "x", "1", "abc", "-5", "", "10", "4", "",          # opção inválida; cálculo com entradas inválidas e padrão
        "2", "s", "7", "",                                  # comparar usando os mesmos dados e a estimativa de custo
        "7", "aquecedor solar compensa?", "n",              # pergunta livre
        "7", "qual a cor do ceu", "7", "voltar",            # pergunta fora do escopo e voltar
        "5", "0",
    ])

    def entrada_falsa(prompt=""):
        valor = next(roteiro)
        print(f"{prompt}{valor}")
        return valor

    builtins.input = entrada_falsa
    iniciar()


def modo_teste():
    """Roda o assistente registrando a sessão de forma anônima (tempos, contagens e opções)."""
    global SESSAO
    SESSAO = Sessao()
    print("\n=== MODO DE TESTE ===")
    print("Vou registrar apenas: tempo, número de erros de digitação e quais opções você usou.")
    print("Nada do que você digitar é salvo. Use o assistente com naturalidade.")
    try:
        iniciar()
    finally:
        caminho = SESSAO.salvar()
        print(f"\nSeu código de sessão é: {SESSAO.codigo}")
        print("1) Anote esse código e informe-o no formulário de perguntas.")
        print(f"2) Envie o arquivo abaixo para quem pediu o teste (por WhatsApp, por exemplo):\n   {caminho}")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--teste" in sys.argv:
        modo_teste()
    else:
        iniciar()
