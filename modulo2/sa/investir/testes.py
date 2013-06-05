import io
import random
import unittest

from sqlalchemy import Column, Integer, String, MetaData

from tabelas import (extrair_nome, extrair_campos, extrair_chaves_primarias,
                     analisar_linha, montar_coluna, montar_tabela,
                     montar_todas_as_tabelas,
                     FormatoInvalido)

class TestesCriarTabelas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with io.open('investir.rdb', encoding='utf-8') as fixture:
            cls.arquivo_esquema = fixture.read()

    def setUp(self):
        self.seq = range(10)
        self.linha_esquema = '''@carteira_fundos(cod_contribuinte/char,simbolo/char,cotas/numeric):cod_contribuinte,simbolo'''
        self.metadata = MetaData()

    def test_extrair_nome_tabela(self):
        nome_tabela = extrair_nome(self.linha_esquema)
        self.assertEqual('carteira_fundos', nome_tabela)

    def test_extrair_nome_tabela_sem_arroba(self):
        with self.assertRaises(FormatoInvalido):
            extrair_nome('carteira_fundos(cod_contribuinte/char,simbolo/char,cotas/numeric):cod_contribuinte,simbolo')

    def test_extrair_nomes_dos_campos_deve_ser_uma_lista_de_duplas(self):
        campos = extrair_campos(self.linha_esquema)
        campo, tipo = campos[0]
        self.assertEqual('cod_contribuinte', campo)
        self.assertEqual('char', tipo)

    def test_extrair_chaves_primarias(self):
        campos = extrair_chaves_primarias(self.linha_esquema)
        self.assertEqual(campos[0], 'cod_contribuinte')
        self.assertEqual(campos[1], 'simbolo')

    def test_analisar_linha(self):
        nome_tabela, campos = analisar_linha(self.linha_esquema)
        self.assertEqual(nome_tabela, 'carteira_fundos')
        self.assertListEqual(campos[-1], ['cotas', 'numeric', False])
        self.assertListEqual(campos[0], ['cod_contribuinte', 'char', True])

    def test_montar_coluna_pk(self):
        nome_tabela, campos = analisar_linha(self.linha_esquema)
        coluna = montar_coluna(*campos[0])
        self.assertIsInstance(coluna.type, String)
        self.assertEqual(coluna.name, 'cod_contribuinte')
        self.assertTrue(coluna.primary_key)

    def test_montar_coluna_sem_pk(self):
        nome_tabela, campos = analisar_linha(self.linha_esquema)
        coluna = montar_coluna(*campos[-1])
        self.assertIsInstance(coluna.type, Integer)
        self.assertEqual(coluna.name, 'cotas')
        self.assertFalse(coluna.primary_key)

    def test_montar_tabela(self):
        tabela = montar_tabela(self.linha_esquema, self.metadata)
        self.assertEqual(tabela.name, 'carteira_fundos')
        self.assertEqual(len(tabela.c), 3)

    def test_montar_todas_as_tabelas(self):
        tabelas = montar_todas_as_tabelas(self.arquivo_esquema, self.metadata)
        self.assertEquals(6, len(tabelas))


if __name__ == '__main__':
    unittest.main()
