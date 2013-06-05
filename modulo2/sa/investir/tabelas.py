# coding: utf-8
import io
import os

import sqlalchemy as sa

class FormatoInvalido(ValueError):
    pass

def extrair_nome(linha_esquema):
    if not linha_esquema.startswith('@'):
        raise FormatoInvalido()
    return linha_esquema.split('(')[0][1:]

def extrair_campos(linha_esquema):
    partes = (linha_esquema.split('(')[1]
                           .split(')')[0]
                           .split(','))

    campos = []
    for parte in partes:
        campos.append(parte.split('/'))
    return campos

def extrair_chaves_primarias(linha_esquema):
    return linha_esquema.split(':')[1].split(',')

def analisar_linha(linha_esquema):
    nome, campos, chaves = (extrair_nome(linha_esquema),
                            extrair_campos(linha_esquema),
                            extrair_chaves_primarias(linha_esquema),)
    for campo in campos:
        campo.append(campo[0] in chaves)
    return nome, campos

def montar_coluna(campo, tipo, chave):
    tipos = {
        'numeric': sa.Integer,
        'char': sa.String
    }
    return sa.Column(campo, tipos[tipo], primary_key=chave)

def montar_tabela(linha_esquema, metadata):
    nome, campos = analisar_linha(linha_esquema)
    colunas = [montar_coluna(campo, tipo, chave)
                    for campo, tipo, chave in campos]
    return sa.Table(nome, metadata, *colunas)

def montar_todas_as_tabelas(contenido_do_arquivo, metadata):
    tabelas = [montar_tabela(line, metadata)
                    for line in contenido_do_arquivo.split('\n') if line.startswith('@')]

    return tabelas

def main(filename):
    url = 'sqlite:///%s.sqlite' % os.path.splitext(filename)[0]
    engine = sa.create_engine(url, echo=True)

    metadata = sa.MetaData()

    with io.open(filename, encoding='utf-8') as f:
        montar_todas_as_tabelas(f.read(), metadata)
    metadata.create_all(engine)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
