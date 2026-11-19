# -*- coding: utf-8 -*-
"""Extrai da base SAMP (ANEEL) o recorte da Enel SP (sigla ELETROPAULO) em 2025.

Entrada : dados/base_residencial_distribuidora_mes.csv (gerada por dados/prep_base.py a partir do samp-2025.csv)
Saída   : dados/samp_enel_sp_2025.csv
"""
import os
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
base = pd.read_csv(os.path.join(PASTA, "base_residencial_distribuidora_mes.csv"))
enel = base[base["SigAgenteDistribuidora"] == "ELETROPAULO"].sort_values("mes")
cols = ["mes", "consumidores", "kwh_tusd", "receita_energia", "consumo_medio_kwh",
        "tarifa_media_rs_kwh", "pct_baixa_renda"]
enel[cols].round(4).to_csv(os.path.join(PASTA, "samp_enel_sp_2025.csv"), index=False)
print(enel[cols].round(3).to_string(index=False))
