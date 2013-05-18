import io
import re

from sqlalchemy import create_engine

import models

engine = create_engine('sqlite:///:memory:', echo=True)

FIXTURE = 'data/invest.rdb'

RE_TABLE = re.compile(r'^@(\w+)\(')

def create_tables():
    models.Base.metadata.create_all(engine)

def load_tables():
    model_tables = {name.lower(): model.__tablename__
                    for name, model in models.__dict__.items()
                    if hasattr(model, '__tablename__')}
    with io.open(FIXTURE, encoding='utf-8') as fixture:
        for line in fixture:
            table_prefix = RE_TABLE.match(line)
            if table_prefix:
                table_prefix = table_prefix.group(1)
                table_key = table_prefix.lower() + 'table'
                table_name = model_tables[table_key]
                print table_prefix, '\t', table_name


load_tables()



