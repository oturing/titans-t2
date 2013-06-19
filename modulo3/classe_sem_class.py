# coding: utf-8

"""
Como criar uma classe sem uma declaração ``class``

    >>> p = Pessoa('Fulano')
    >>> p.nome
    'Fulano'
    >>> p.idade
    0
    >>> print p
    <Pessoa 'Fulano'>

"""

def init(self, nome):
    self.nome = nome
def repr_(self):
    return '<%s %r>' % (self.__class__.__name__, self.nome)

Pessoa = type('Pessoa', (object,), {'idade':0, '__init__':init,
                '__repr__':lambda self: '<%s %r>' % (self.__class__.__name__, self.nome)})


Pessoa1 = type('Pessoa', (object,), {'idade':0, '__init__':init, '__repr__':repr_})

class Pessoa0(object):
    idade = 0
    def __init__(self, nome):
        self.nome = nome
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.nome)
