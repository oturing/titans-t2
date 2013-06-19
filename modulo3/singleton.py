# coding: utf-8

"""
Singleton: devolve sempre a mesma instância

    >>> o1 = Unico()
    >>> o2 = Unico()
    >>> o1 is o2
    True

"""

class Unico(object):
    '''devolve sempre a mesma instância'''
    a_instancia = None
    def __new__(cls, *args, **kwargs):
        if cls.a_instancia is None:
            cls.a_instancia = super(Unico, cls).__new__(cls, *args, **kwargs)
        return cls.a_instancia
