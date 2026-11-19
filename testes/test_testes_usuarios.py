# -*- coding: utf-8 -*-
"""Testes da automação dos testes com usuários (modo --teste e consolidar_testes.py). Usam dados temporários."""
import builtins
import csv
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "assistente"))
sys.path.insert(0, os.path.join(RAIZ, "testes_usuarios"))
import assistente as at  # noqa: E402
import consolidar_testes as ct  # noqa: E402


def rodar_sessao(entradas):
    it = iter(entradas)
    original = builtins.input
    builtins.input = lambda prompt="": next(it)
    at.SESSAO = at.Sessao()
    try:
        with redirect_stdout(io.StringIO()):
            at.iniciar()
        return at.SESSAO
    finally:
        builtins.input = original


class TestTelemetria(unittest.TestCase):
    def tearDown(self):
        at.SESSAO = None

    def test_registra_erros_opcoes_e_tempo_da_s1(self):
        sessao = rodar_sessao(["x", "1", "abc", "", "", "", "", "7", "aquecedor solar compensa?", "n", "0"])
        self.assertGreaterEqual(sessao.erros, 2)               # opção inválida "x" e entrada "abc"
        self.assertEqual(sessao.opcoes, ["1", "7"])  # "0" (sair) não conta como opção usada
        self.assertIsNotNone(sessao.t_s1)
        self.assertEqual(sessao.topicos, ["solar_custo"])

    def test_arquivo_nao_guarda_texto_digitado(self):
        sessao = rodar_sessao(["7", "aquecedor solar compensa?", "n", "0"])
        with tempfile.TemporaryDirectory() as pasta:
            caminho = sessao.salvar(pasta)
            with open(caminho, encoding="utf-8") as f:
                conteudo = f.read()
        self.assertNotIn("aquecedor solar compensa", conteudo)
        self.assertIn(sessao.codigo, conteudo)
        self.assertTrue(sessao.codigo.startswith("T-"))


class TestConsolidacao(unittest.TestCase):
    CAB = ["Carimbo de data/hora", "Código da sessão (aparece no final do teste, ex.: T-7K2Q)",
           "Você faz parte do grupo do projeto?", "Faixa etária",
           "S1. Consegui descobrir quanto o meu chuveiro gasta por mês",
           "S2. Consegui comparar o aquecedor solar com o banho mais curto",
           "S3. Consegui perguntar com as minhas palavras e recebi uma resposta útil",
           "S4. Quando digitei algo inválido, a mensagem me ajudou",
           "Entendi o que o assistente me disse.", "As orientações me ajudariam a decidir como economizar.",
           "O que foi confuso? Quais dúvidas você teve?", "Sugestões: o que você mudaria?"]

    def _montar(self, pasta, linhas_forms, sessoes):
        os.makedirs(os.path.join(pasta, "sessoes"))
        for s in sessoes:
            with open(os.path.join(pasta, "sessoes", s["codigo"] + ".json"), "w", encoding="utf-8") as f:
                json.dump(s, f)
        with open(os.path.join(pasta, "respostas_forms.csv"), "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(self.CAB)
            w.writerows(linhas_forms)

    def test_junta_formulario_e_sessao_pelo_codigo(self):
        sessao = {"codigo": "T-AAAA", "inicio": "2026-11-18T10:00:00", "fim": "2026-11-18T10:05:00",
                  "erros_de_entrada": 2, "tempo_s1_segundos": 41.5}
        forms = [["x", "t-aaaa", "Não, sou externo", "50+", "Com ajuda", "Sozinho(a)", "Não testei", "Sim",
                  "4", "5", "Não sabia a potência", "Explicar a potência"]]
        with tempfile.TemporaryDirectory() as pasta, redirect_stdout(io.StringIO()):
            self._montar(pasta, forms, [sessao])
            linhas, avisos = ct.main(pasta)
            with open(os.path.join(pasta, "registro_testes.csv"), encoding="utf-8") as f:
                conteudo = f.read()
            with open(os.path.join(pasta, "resumo_testes.md"), encoding="utf-8") as f:
                resumo = f.read()
        self.assertEqual(avisos, [])
        l = linhas[0]
        self.assertEqual(l["codigo"], "T-AAAA")
        self.assertEqual(l["grupo_ou_externo"], "externo")
        self.assertEqual(l["situacoes_testadas"], "S1;S2;S4")
        self.assertEqual(l["tempo_s1_segundos"], 41.5)
        self.assertEqual(l["erros_de_entrada"], 2)
        self.assertEqual(l["data"], "18/11/2026")
        self.assertIn("Não sabia a potência", l["comentarios"])
        self.assertIn("T-AAAA", conteudo)
        self.assertIn("Participantes: **1**", resumo)

    def test_preserva_ajuste_gerado_ao_reexecutar(self):
        sessao = {"codigo": "T-DDDD", "inicio": "2026-11-18T10:00:00", "fim": "2026-11-18T10:05:00",
                  "erros_de_entrada": 0, "tempo_s1_segundos": 30.0}
        forms = [["x", "T-DDDD", "Sim, sou do grupo", "30-39", "Sozinho(a)", "Sozinho(a)", "Sozinho(a)", "Sim",
                  "5", "4", "", ""]]
        with tempfile.TemporaryDirectory() as pasta, redirect_stdout(io.StringIO()):
            self._montar(pasta, forms, [sessao])
            ct.main(pasta)
            caminho = os.path.join(pasta, "registro_testes.csv")
            with open(caminho, encoding="utf-8", newline="") as f:
                linhas = list(csv.DictReader(f))
            linhas[0]["ajuste_gerado"] = "Explicação da potência no assistente"
            with open(caminho, "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=ct.CAMPOS)
                w.writeheader()
                w.writerows(linhas)
            novas, _ = ct.main(pasta)
        self.assertEqual(novas[0]["ajuste_gerado"], "Explicação da potência no assistente")

    def test_avisa_sessao_sem_formulario_e_formulario_sem_sessao(self):
        sessao = {"codigo": "T-BBBB", "inicio": "2026-11-18T11:00:00", "fim": "2026-11-18T11:05:00",
                  "erros_de_entrada": 0, "tempo_s1_segundos": None}
        forms = [["x", "T-CCCC", "Sim, sou do grupo", "30-39", "Sozinho(a)", "Sozinho(a)", "Sozinho(a)", "Sim",
                  "5", "5", "", ""]]
        with tempfile.TemporaryDirectory() as pasta, redirect_stdout(io.StringIO()):
            self._montar(pasta, forms, [sessao])
            linhas, avisos = ct.main(pasta)
        self.assertEqual(len(linhas), 2)
        self.assertEqual(len(avisos), 2)
        self.assertEqual({l["grupo_ou_externo"] for l in linhas}, {"", "grupo"})


if __name__ == "__main__":
    unittest.main()
