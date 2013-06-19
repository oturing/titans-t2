# coding: utf-8

"""
Definimos uma subclasse de ModeloOrdenado:

    >>> class ItemPedidoResistor(ModeloOrdenado):
    ...     quantidade = Quantidade()
    ...     resistencia = Quantidade()
    ...     tolerancia = Quantidade()
    ...     preco = Quantidade()
    ...
    >>> ItemPedidoResistor.listar_campos()
    ['quantidade', 'resistencia', 'tolerancia', 'preco']

Sua missão é fazer o método ``listar_campos`` gerar a lista dos campos
na ordem em que eles foram definidos na classe ItemPedidoResistor

"""

from pedidos_meta import Modelo, Quantidade

class ModeloOrdenado(Modelo):
    @classmethod
    def listar_campos(cls):
        listagem = []
        for nome, atr in cls.__dict__.items():
            if isinstance(atr, Quantidade):
                listagem.append(nome)
        return listagem



