# -*- coding: utf-8 -*-
"""Testes automáticos dos cálculos. Rodar na raiz do repositório: python -m unittest discover -s testes -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "calculos"))
import energia as en  # noqa: E402


class TestEnergia(unittest.TestCase):
    def setUp(self):
        self.p = en.carregar_premissas()

    def test_energia_do_banho_de_referencia(self):
        # 5,5 kW x (12/60) h x 4 pessoas x 30 dias = 132 kWh/mês
        self.assertAlmostEqual(en.energia_kwh_mes(5500, 12, 4, 30), 132.0, places=6)

    def test_um_banho_de_10_minutos_usa_cerca_de_0_92_kwh(self):
        self.assertAlmostEqual(en.energia_kwh_mes(5500, 10, 1, 1), 0.9167, places=3)

    def test_custo(self):
        self.assertAlmostEqual(en.custo_rs(100, 1.0135), 101.35, places=6)

    def test_tarifa_estimada(self):
        self.assertAlmostEqual(en.tarifa_com_tributos_estimada(self.p), 1.0135, places=3)

    def test_consistencia_com_simulacao_da_cemig(self):
        economia_kwh = en.energia_kwh_mes(5500, 12, 4) - en.energia_kwh_mes(5500, 8, 4)
        self.assertAlmostEqual(economia_kwh, 44.0, places=6)
        self.assertAlmostEqual(50.54 / economia_kwh, 1.1486, places=3)

    def test_payback(self):
        self.assertAlmostEqual(en.payback_anos(4500, 1125), 4.0, places=6)
        self.assertIsNone(en.payback_anos(0, 100))
        self.assertIsNone(en.payback_anos(4500, 0))

    def test_comparacao_cenario_base(self):
        c = en.cenarios_solares(self.p)["base"]
        l = en.comparar_alternativas(5500, 12, 8, 4, 1.0135, c["fracao"], c["custo"], self.p)
        atual, a, b, ab = l
        self.assertAlmostEqual(atual["kwh_mes"], 132.0, places=6)
        self.assertAlmostEqual(a["kwh_mes"], 88.0, places=6)
        self.assertAlmostEqual(b["kwh_mes"], 52.8, places=6)
        self.assertAlmostEqual(ab["kwh_mes"], 35.2, places=6)
        self.assertAlmostEqual(b["payback_anos"], 4.7, places=1)
        self.assertEqual(atual["investimento_rs"], 0.0)
        self.assertGreater(ab["economia_ano_rs"], b["economia_ano_rs"])

    def test_exemplo_numerico_do_idec(self):
        # Idec (R3): chuveiro de 5.500 W, 1 hora por dia, 30 dias = 165 kWh; a R$ 0,74/kWh, cerca de R$ 122,10
        kwh = en.energia_kwh_mes(5500, 60, 1, 30)
        self.assertAlmostEqual(kwh, 165.0, places=6)
        self.assertAlmostEqual(en.custo_rs(kwh, 0.74), 122.10, places=2)

    def test_pmee_do_coletor_de_referencia_bate_com_a_ficha_tecnica(self):
        # R12: 1,5 Maxime = 1,46 m2 e 121,4 kWh/mês (classe A, acima de 80,3 kWh/m2.mês)
        nominal = self.p["solar_area_m2"] * self.p["solar_pmee_kwh_m2_mes"]
        self.assertAlmostEqual(nominal, 121.4, places=1)
        self.assertGreater(self.p["solar_pmee_kwh_m2_mes"], 80.3)

    def test_nenhum_cenario_solar_excede_a_alegacao_maxima_do_fabricante(self):
        for c in en.cenarios_solares(self.p).values():
            self.assertLessEqual(c["fracao"], 0.70 + 1e-9)

    def test_producao_solar_nominal(self):
        self.assertAlmostEqual(en.producao_solar_nominal_kwh_mes(self.p), 97.12, places=1)


if __name__ == "__main__":
    unittest.main()
