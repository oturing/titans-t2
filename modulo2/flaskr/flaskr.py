# coding: utf-8

# todos os imports
import sqlite3
import flask

# configuração
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# criar nossa pequena aplicação :)
app = flask.Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()
