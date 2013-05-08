# coding: utf-8

from __future__ import unicode_literals

import os
import unittest
import tempfile

import pymongo

import flask

import flaskr

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        flaskr.app.config['DATABASE'] = 'FLASKR_TEST_DB'
        flaskr.app.config['TESTING'] = True
        self.client = flaskr.app.test_client()

    def tearDown(self):
        '''TODO: fechar conexao com o MongoDB'''
        flaskr.conectar_bd().drop_collection('posts')

    def testar_conexao(self):
        db = flaskr.conectar_bd()
        self.assertIsInstance(db, pymongo.database.Database)

    def testar_bd_vazio(self):
        res = self.client.get('/')
        self.assertIn(b'nenhuma entrada', res.data)

    def fazer_login(self, username, password):
        return self.client.post('/entrar',
                data=dict(username=username,
                          password=password),
                follow_redirects=True)

    def testar_login(self):
        rv = self.fazer_login('admin', 'default')
        self.assertIn(b'Login OK', rv.data)

    @unittest.skip('TODO: fazer com mock?')
    def testar_login_seta_secao(self):
        dados = dict(username='admin',
                     password='default')
        with flaskr.app.test_request_context('/entrar',
                method='POST', data=dados):
            flaskr.app.preprocess_request()
            self.assertTrue(flask.session['logado'])

    def testar_login_invalido(self):
        rv = self.fazer_login('adminx', 'default')
        self.assertIn(b'Usuário inválido', rv.data)
        rv = self.fazer_login('admin', 'defaultx')
        self.assertIn(b'Senha inválida', rv.data)

    def testar_logout(self):
        rv = self.client.get('/sair', follow_redirects=True)
        self.assertIn(b'Logout OK', rv.data)

    def testar_nova_entrada(self):
        self.fazer_login('admin', 'default')
        rv = self.client.post('/inserir', data=dict(
            titulo='<Olá>',
            texto='<strong>HTML</strong> é permitido aqui'
        ), follow_redirects=True)
        self.assertEquals(rv.status_code, 200)
        self.assertNotIn(b'nenhuma entrada', rv.data)
        self.assertIn(b'&lt;Olá&gt;', rv.data)
        self.assertIn(b'<strong>HTML</strong> é permitido aqui', rv.data)


if __name__ == '__main__':
    unittest.main()
