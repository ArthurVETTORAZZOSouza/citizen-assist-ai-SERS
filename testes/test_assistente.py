# -*- coding: utf-8 -*-
"""Testes do assistente: entendimento de perguntas e tratamento de entradas inválidas."""
import builtins
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "assistente"))
import assistente as at  # noqa: E402


class TestPerguntas(unittest.TestCase):
    def test_topicos_conhecidos(self):
        casos = {
            "Quanto gasta um chuveiro elétrico?": "custo_chuveiro",
            "como economizar no banho": "uso_consciente",
            "aquecedor solar compensa?": "solar_custo",
            "e o CO2? é sustentável?": "emissoes",
            "tenho direito à tarifa social?": "baixa_renda",
        }
        for pergunta, esperado in casos.items():
            self.assertEqual(at.responder_texto(pergunta), esperado, pergunta)

    def test_pergunta_fora_do_escopo_ou_vazia(self):
        self.assertIsNone(at.responder_texto("qual a cor do ceu"))
        self.assertIsNone(at.responder_texto("   "))
        self.assertIsNone(at.responder_texto(""))

    def test_pergunta_muito_longa_nao_quebra(self):
        at.responder_texto("chuveiro " * 1000)

    def test_melhorias_negacao_e_novos_topicos(self):
        self.assertEqual(
            at.responder_texto(
                "moro em imovel alugado, nao posso instalar aquecedor solar, quanto economizo mudando a chave para verao?"),
            "chave_verao_inverno",
        )
        self.assertEqual(
            at.responder_texto("moro em imovel alugado e nao posso instalar aquecedor solar"),
            "imovel_alugado",
        )
        self.assertEqual(
            at.responder_texto("mudar a chave do chuveiro do inverno para o verao economiza?"),
            "chave_verao_inverno",
        )

class TestComparacaoComOrcamento(unittest.TestCase):
    def _rodar_comparacao(self, entradas, perfil):
        it = iter(entradas)
        original = builtins.input
        builtins.input = lambda prompt="": next(it)
        saida = io.StringIO()
        try:
            with redirect_stdout(saida):
                at.opcao_comparar(perfil)
        finally:
            builtins.input = original
        return saida.getvalue()

    def test_orcamento_do_usuario_vale_para_os_tres_cenarios(self):
        perfil = {"potencia_w": 5500, "minutos": 12, "pessoas": 4, "tarifa": 1.01}
        texto = self._rodar_comparacao(["s", "", "3800"], perfil)
        self.assertEqual(texto.count("3.800"), 3)

    def test_aviso_para_casa_pequena_sem_orcamento(self):
        perfil = {"potencia_w": 5500, "minutos": 12, "pessoas": 2, "tarifa": 1.01}
        texto = self._rodar_comparacao(["s", "", ""], perfil)
        self.assertIn("Prefira um orçamento real", texto)


class TestEntradas(unittest.TestCase):
    def _rodar(self, entradas, **kw):
        it = iter(entradas)
        original = builtins.input
        builtins.input = lambda prompt="": next(it)
        try:
            with redirect_stdout(io.StringIO()):
                return at.ler_numero("pergunta", **kw)
        finally:
            builtins.input = original

    def test_valida_e_aceita_virgula(self):
        self.assertEqual(self._rodar(["abc", "-3", "5,5"], minimo=1, maximo=60, padrao=12), 5.5)

    def test_valor_acima_do_maximo_e_rejeitado(self):
        self.assertEqual(self._rodar(["9999", "30"], minimo=1, maximo=60, padrao=12), 30.0)

    def test_enter_usa_padrao(self):
        self.assertEqual(self._rodar([""], minimo=1, maximo=60, padrao=12), 12.0)

    def test_tres_erros_usam_padrao(self):
        self.assertEqual(self._rodar(["a", "b", "c"], minimo=1, maximo=60, padrao=12), 12.0)

    def test_voltar_levanta_excecao(self):
        with self.assertRaises(at.VoltarAoMenu):
            self._rodar(["voltar"], minimo=1, maximo=60, padrao=12)

    def test_nan_e_infinito_sao_rejeitados(self):
        self.assertEqual(self._rodar(["nan", "inf", "7"], minimo=1, maximo=60, padrao=12), 7.0)


if __name__ == "__main__":
    unittest.main()
