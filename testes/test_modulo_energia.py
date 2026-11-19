# -*- coding: utf-8 -*-
"""Testes do ponto de integração (assistente/modulo_energia.py)."""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "assistente"))
import modulo_energia as me  # noqa: E402


class TestModuloEnergia(unittest.TestCase):
    def test_resposta_traz_texto_referencias_e_aviso(self):
        r = me.responder_energia("aquecedor solar compensa?")
        self.assertEqual(r["topico"], "solar_custo")
        self.assertTrue(r["texto"])
        self.assertTrue(r["referencias"])
        self.assertIn("estimativa", r["aviso"].lower())

    def test_pergunta_fora_do_escopo(self):
        r = me.responder_energia("qual a cor do ceu")
        self.assertIsNone(r["topico"])
        self.assertTrue(r["texto"])

    def test_calcular_banho(self):
        r = me.calcular_banho(5500, 12, 4, 1.0135)
        self.assertAlmostEqual(r["kwh_mes"], 132.0, places=6)
        self.assertAlmostEqual(r["custo_mes_rs"], 133.782, places=3)

    def test_entradas_invalidas_levantam_erro(self):
        for args in [(-5, 12, 4), (5500, 0, 4), (5500, 12, 99), ("abc", 12, 4)]:
            with self.assertRaises(ValueError):
                me.calcular_banho(*args)

    def test_comparar_banho_e_orcamento(self):
        r = me.comparar_banho(5500, 12, 8, 4, 1.0135)
        self.assertEqual(len(r["alternativas"]), 4)
        self.assertEqual(set(r["cenarios_solares"]), {"conservador", "base", "otimista"})
        r2 = me.comparar_banho(5500, 12, 8, 4, 1.0135, orcamento=3800)
        for linha in r2["cenarios_solares"].values():
            self.assertEqual(linha["investimento_rs"], 3800)

    def test_minutos_consciente_nao_pode_superar_o_atual(self):
        with self.assertRaises(ValueError):
            me.comparar_banho(5500, 10, 15, 4)


if __name__ == "__main__":
    unittest.main()
