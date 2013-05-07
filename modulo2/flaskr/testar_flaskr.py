# coding: utf-8

from __future__ import unicode_literals

import os
import unittest
import tempfile

import flask

import flaskr

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.bd_arq, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.client = flaskr.app.test_client()
        flaskr.criar_bd()

    def tearDown(self):
        os.close(self.bd_arq)
        os.unlink(flaskr.app.config['DATABASE'])

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

    def testar_login_invalido(self):
        rv = self.fazer_login('adminx', 'default')
        self.assertIn(b'Usuário inválido', rv.data)
        rv = self.fazer_login('admin', 'defaultx')
        self.assertIn(b'Senha inválida', rv.data)

    def teste_login_logout(self):
        rv = self.client.get('/sair', follow_redirects=True)
        self.assertIn(b'Logout OK', rv.data)


if __name__ == '__main__':
    unittest.main()
