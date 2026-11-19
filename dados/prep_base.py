import os
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(PASTA)

ARQ = next(
    (c for c in (os.path.join(PASTA, "samp-2025.csv"), os.path.join(RAIZ, "samp-2025.csv"), "samp-2025.csv") if os.path.exists(c)),
    os.path.join(PASTA, "samp-2025.csv"),
)
SAIDA_SUB = os.path.join(PASTA, "base_residencial_subclasse.csv")
SAIDA_DM = os.path.join(PASTA, "base_residencial_distribuidora_mes.csv")

USAR = ["SigAgenteDistribuidora", "NomTipoMercado", "DscClasseConsumoMercado",
        "DscSubClasseConsumidor", "DscDetalheMercado", "DatCompetencia", "VlrMercado"]

MEDIDAS = {
    "Energia TUSD (kWh)": "kwh_tusd",
    "Energia TE (kWh)": "kwh_te",
    "Energia Consumida (kWh)": "kwh_consumida",
    "Número de consumidores": "consumidores",
    "Número de Consumidores": "consumidores",
    "Receita Energia (R$)": "receita_energia",
    "Receita Bandeiras (R$)": "receita_bandeiras",
    "ICMS (R$)": "icms",
}

# 1) leitura em partes, já filtrando Residencial + Regular + medidas de interesse
pedacos = []
for enc in ("utf-8-sig", "latin-1"):
    try:
        for parte in pd.read_csv(ARQ, sep=",", encoding=enc, usecols=USAR,
                                 chunksize=500_000, dtype=str):
            filtro = (
                (parte["DscClasseConsumoMercado"] == "Residencial")
                & (parte["NomTipoMercado"] == "Regular")
                & (parte["DscDetalheMercado"].isin(MEDIDAS))
            )
            pedacos.append(parte[filtro])
        break
    except UnicodeDecodeError:
        pedacos = []
        continue

df = pd.concat(pedacos, ignore_index=True)
print("Linhas residenciais (Regular) lidas:", len(df))

# 2) limpeza do valor (vírgula decimal) e nome das medidas
df["valor"] = pd.to_numeric(df["VlrMercado"].str.replace(",", ".", regex=False),
                            errors="coerce")
print("Valores não numéricos:", int(df["valor"].isna().sum()))
df["medida"] = df["DscDetalheMercado"].map(MEDIDAS)
df["mes"] = df["DatCompetencia"].str[:7]

# 3) pivotagem: uma linha por distribuidora x mês x subclasse
sub = df.pivot_table(index=["SigAgenteDistribuidora", "mes", "DscSubClasseConsumidor"],
                     columns="medida", values="valor", aggfunc="sum").reset_index()
sub.columns.name = None
for c in set(MEDIDAS.values()):
    if c not in sub.columns:
        sub[c] = float("nan")
sub.to_csv(SAIDA_SUB, index=False)

# 4) agregação: uma linha por distribuidora x mês, com variáveis derivadas
sub["baixa_renda"] = sub["DscSubClasseConsumidor"].str.contains(
    "baixa renda|Tarifa Social", case=False, na=False)
sub["cons_baixa_renda"] = sub["consumidores"].where(sub["baixa_renda"], 0)

dm = sub.groupby(["SigAgenteDistribuidora", "mes"], as_index=False).agg(
    kwh_tusd=("kwh_tusd", "sum"), kwh_te=("kwh_te", "sum"),
    consumidores=("consumidores", "sum"), cons_baixa_renda=("cons_baixa_renda", "sum"),
    receita_energia=("receita_energia", "sum"),
    receita_bandeiras=("receita_bandeiras", "sum"), icms=("icms", "sum"))

dm["consumo_medio_kwh"] = dm["kwh_tusd"] / dm["consumidores"]
dm["tarifa_media_rs_kwh"] = dm["receita_energia"] / dm["kwh_tusd"]
dm["conta_media_rs"] = dm["receita_energia"] / dm["consumidores"]
dm["pct_baixa_renda"] = 100 * dm["cons_baixa_renda"] / dm["consumidores"]
dm.to_csv(SAIDA_DM, index=False)

# 5) relatório de conferência
print("\nBase final:", dm.shape[0], "linhas;", dm["SigAgenteDistribuidora"].nunique(),
      "distribuidoras;", dm["mes"].nunique(), "meses")
print("\nNulos por coluna:\n", dm.isna().sum().to_string())
cols = ["consumo_medio_kwh", "tarifa_media_rs_kwh", "conta_media_rs", "pct_baixa_renda"]
print("\nResumo:\n", dm[cols].describe().round(2).to_string())
print("\nCorrelação kwh_tusd x kwh_te:", round(dm["kwh_tusd"].corr(dm["kwh_te"]), 4))
