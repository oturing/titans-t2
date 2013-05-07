# coding: utf-8

from __future__ import unicode_literals

# todos os imports
from contextlib import closing
import sqlite3
import flask
from flask import g

# configuração
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = b'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# criar nossa pequena aplicação :)
app = flask.Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

def criar_bd():
    with closing(conectar_bd()) as bd:
        with app.open_resource('esquema.sql') as sql:
            bd.cursor().executescript(sql.read())
        bd.commit()

@app.before_request
def pre_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def encerrar_requisicao(exception):
    g.bd.close()

@app.route('/')
def exibir_entradas():
    sql = '''select titulo, texto from entradas order by id desc'''
    cur = g.bd.execute(sql)
    entradas = [dict(titulo=titulo, texto=texto)
                    for titulo, texto in cur.fetchall()]
    return flask.render_template('exibir_entradas.html', entradas=entradas)

@app.route('/inserir', methods=['POST'])
def inserir_entrada():
    if not flask.session.get('logado'):
        flask.abort(401)
    sql = '''insert into entradas (titulo, texto) values (?, ?)'''
    g.bd.execute(sql, [flask.request.form['titulo'],
                       flask.request.form['texto']])
    g.bd.commit()
    flask.flash('Nova entrada registrada com sucesso')
    return flask.redirect(flask.url_for('exibir_entradas'))

@app.route('/entrar', methods=['GET', 'POST'])
def login():
    erro = None
    if flask.request.method == 'POST':
        if flask.request.form['username'] != app.config['USERNAME']:
            erro = 'Usuário inválido'
        elif flask.request.form['password'] != app.config['PASSWORD']:
            erro = 'Senha inválida'
        else:
            flask.session['logado'] = True
            flask.flash('Login OK')
            return flask.redirect(flask.url_for('exibir_entradas'))
    return flask.render_template('login.html', erro=erro)

@app.route('/sair')
def logout():
    flask.session.pop('logado', None)
    flask.flash('Logout OK')
    return flask.redirect(flask.url_for('exibir_entradas'))



if __name__ == '__main__':
    app.run()
